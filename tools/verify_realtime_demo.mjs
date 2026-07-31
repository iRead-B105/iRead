const baseUrl = process.env.IREAD_API_BASE_URL ?? 'http://localhost:8080'
const email = process.env.IREAD_DEMO_EMAIL ?? 'demo@iread.local'
const password = process.env.IREAD_DEMO_PASSWORD ?? 'demo1234'
const studentId = process.env.IREAD_DEMO_STUDENT_ID ?? '2001'
const limitMs = Number(process.env.IREAD_REALTIME_LIMIT_MS ?? '3000')

async function api(path, { token, method = 'GET', body } = {}) {
  const response = await fetch(`${baseUrl}${path}`, {
    method,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  const text = await response.text()
  if (!response.ok) {
    throw new Error(`${method} ${path} -> ${response.status}: ${text.slice(0, 300)}`)
  }
  return text ? JSON.parse(text) : null
}

async function nextEvent(path, token, resource, changeType) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 10_000)
  try {
    const response = await fetch(`${baseUrl}${path}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'text/event-stream',
      },
      signal: controller.signal,
    })
    if (!response.ok || !response.body) {
      throw new Error(`SSE ${path} -> ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    while (true) {
      const { done, value } = await reader.read()
      if (done) throw new Error(`SSE ${path} ended before the expected event`)
      buffer += decoder.decode(value, { stream: true })
      const blocks = buffer.split(/\r?\n\r?\n/)
      buffer = blocks.pop() ?? ''
      for (const block of blocks) {
        const data = block
          .split(/\r?\n/)
          .filter((line) => line.startsWith('data:'))
          .map((line) => line.slice(5).trimStart())
          .join('\n')
        if (!data) continue
        const event = JSON.parse(data)
        if (event.resource === resource && event.changeType === changeType) {
          controller.abort()
          return { event, receivedAt: Date.now() }
        }
      }
    }
  } finally {
    clearTimeout(timeout)
  }
}

const admin = (await api('/api/auth/admin/login', {
  method: 'POST',
  body: { email, password },
})).data
const bootstrap = (await api('/api/auth/app/teacher-login', {
  method: 'POST',
  body: { email, password },
})).data
const learner = (await api('/api/auth/app/student-login', {
  token: bootstrap.teacherSessionToken,
  method: 'POST',
  body: { studentId },
})).data
const current = (await api(`/api/admin/training/${studentId}/current`, {
  token: admin.accessToken,
})).data

if (current.trainings.length < 2) {
  throw new Error('The demo curriculum needs at least two trainings')
}

const editableTraining = current.trainings[1]
const firstTraining = current.trainings[0]
const wordName = `sync-check-${Date.now()}`
let addedWordId = null

const learnerWait = nextEvent(
  '/api/app/realtime/events',
  learner.accessToken,
  'TRAINING',
  'CONTENT_UPDATED',
)
await new Promise((resolve) => setTimeout(resolve, 250))
const teacherWriteAt = Date.now()

try {
  await api(
    `/api/admin/training/${studentId}/${editableTraining.trainingId}/expected-word`,
    {
      token: admin.accessToken,
      method: 'POST',
      body: { wordName },
    },
  )
  const learnerEvent = await learnerWait
  const words = (await api(
    `/api/admin/training/${studentId}/${editableTraining.trainingId}/expected-word`,
    { token: admin.accessToken },
  )).data.words
  addedWordId = words.find((word) => word.word === wordName)?.wordId ?? null
  if (addedWordId === null) throw new Error('The temporary expected word was not found')

  const adminWait = nextEvent(
    '/api/admin/realtime/events',
    admin.accessToken,
    'TRAINING',
    'RESET',
  )
  await new Promise((resolve) => setTimeout(resolve, 250))
  const learnerWriteAt = Date.now()
  await api(
    `/api/app/training/${studentId}/${firstTraining.trainingId}/session-reset`,
    {
      token: learner.accessToken,
      method: 'POST',
    },
  )
  const adminEvent = await adminWait

  const result = {
    teacherToLearnerMs: learnerEvent.receivedAt - teacherWriteAt,
    learnerToTeacherMs: adminEvent.receivedAt - learnerWriteAt,
    studentId: Number(studentId),
    curriculumId: current.curriculumId,
    editedTrainingId: editableTraining.trainingId,
    learnerTrainingId: firstTraining.trainingId,
  }
  console.log(JSON.stringify(result, null, 2))
  if (
    result.teacherToLearnerMs > limitMs
    || result.learnerToTeacherMs > limitMs
  ) {
    throw new Error(`Realtime propagation exceeded ${limitMs}ms`)
  }
} finally {
  if (addedWordId !== null) {
    await api(
      `/api/admin/training/${studentId}/${editableTraining.trainingId}`
        + `/expected-word/${addedWordId}`,
      {
        token: admin.accessToken,
        method: 'DELETE',
      },
    )
  }
}
