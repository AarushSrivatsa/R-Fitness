<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { apiRequest } from '../lib/api'

type AdminSession = { access_token: string; token_type: 'bearer'; expires_in: number }

type Lead = {
  id: number
  full_name: string
  phone: string
  email: string | null
  fitness_goal: string | null
  preferred_contact: string
  message: string | null
  status: 'new' | 'contacted' | 'converted' | 'closed'
  created_at: string
}

type Plan = {
  id: number
  title: string
  description: string | null
  duration_days: number | null
  price_amount: number | string | null
  price_label: string
  features: string[]
  display_order: number
  is_active: boolean
}

type Overview = { total_leads: number; new_leads: number; active_plans: number }

const session = ref<AdminSession | null>(null)
const email = ref('')
const password = ref('')
const leads = ref<Lead[]>([])
const plans = ref<Plan[]>([])
const overview = ref<Overview>({ total_leads: 0, new_leads: 0, active_plans: 0 })
const loading = ref(false)
const busy = ref(false)
const error = ref('')
const notice = ref('')
const showPlanForm = ref(false)
const draft = reactive({
  title: '',
  description: '',
  duration_days: '',
  price_label: 'Contact for pricing',
  features: '',
})

async function loadDashboard() {
  if (!session.value) return
  loading.value = true
  error.value = ''
  try {
    const token = session.value.access_token
    const [leadRows, planRows, stats] = await Promise.all([
      apiRequest<Lead[]>('/api/v1/admin/leads', { token }),
      apiRequest<Plan[]>('/api/v1/admin/plans', { token }),
      apiRequest<Overview>('/api/v1/admin/overview', { token }),
    ])
    leads.value = leadRows
    plans.value = planRows
    overview.value = stats
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not load admin data.'
  } finally {
    loading.value = false
  }
}

async function login() {
  busy.value = true
  error.value = ''
  try {
    const result = await apiRequest<AdminSession>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: email.value, password: password.value }),
    })
    session.value = result
    sessionStorage.setItem('rf_admin_session', JSON.stringify(result))
    password.value = ''
    await loadDashboard()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to sign in.'
  } finally {
    busy.value = false
  }
}

function logout() {
  sessionStorage.removeItem('rf_admin_session')
  session.value = null
  leads.value = []
  plans.value = []
  notice.value = ''
  error.value = ''
}

async function updateStatus(leadId: number, event: Event) {
  if (!session.value) return
  const status = (event.target as HTMLSelectElement).value as Lead['status']
  try {
    const updated = await apiRequest<Lead>(`/api/v1/admin/leads/${leadId}`, {
      method: 'PATCH',
      token: session.value.access_token,
      body: JSON.stringify({ status }),
    })
    leads.value = leads.value.map((lead) => lead.id === leadId ? updated : lead)
    overview.value.new_leads = leads.value.filter((lead) => lead.status === 'new').length
    notice.value = 'Enquiry updated.'
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not update enquiry.'
  }
}

async function createPlan() {
  if (!session.value) return
  busy.value = true
  error.value = ''
  try {
    const payload = {
      title: draft.title,
      description: draft.description || null,
      duration_days: draft.duration_days ? Number(draft.duration_days) : null,
      price_label: draft.price_label,
      features: draft.features.split('\n').map((item) => item.trim()).filter(Boolean),
    }
    await apiRequest<Plan>('/api/v1/admin/plans', {
      method: 'POST',
      token: session.value.access_token,
      body: JSON.stringify(payload),
    })
    Object.assign(draft, { title: '', description: '', duration_days: '', price_label: 'Contact for pricing', features: '' })
    showPlanForm.value = false
    notice.value = 'Membership plan added.'
    await loadDashboard()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not create membership plan.'
  } finally {
    busy.value = false
  }
}

async function togglePlan(plan: Plan) {
  if (!session.value) return
  try {
    await apiRequest<Plan>(`/api/v1/admin/plans/${plan.id}`, {
      method: 'PATCH',
      token: session.value.access_token,
      body: JSON.stringify({ is_active: !plan.is_active }),
    })
    await loadDashboard()
    notice.value = 'Membership plan updated.'
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not update plan.'
  }
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

onMounted(async () => {
  const savedSession = sessionStorage.getItem('rf_admin_session')
  if (!savedSession) return
  try {
    const parsed = JSON.parse(savedSession) as AdminSession
    if (typeof parsed.access_token !== 'string' || !parsed.access_token) throw new Error('Invalid saved session')
    session.value = parsed
    await loadDashboard()
  } catch {
    sessionStorage.removeItem('rf_admin_session')
    session.value = null
  }
})
</script>

<template>
  <main class="admin-shell">
    <header class="admin-topbar">
      <RouterLink class="brand-mark" to="/">
        <span class="brand-icon">R</span><span class="brand-copy">R<span>FITNESS</span></span>
      </RouterLink>
      <span class="admin-top-label">MANAGEMENT CONSOLE</span>
      <button v-if="session" class="btn btn-outline-light btn-sm" @click="logout">SIGN OUT <i class="bi bi-box-arrow-right ms-1"></i></button>
      <RouterLink v-else to="/" class="admin-back-link"><i class="bi bi-arrow-left me-2"></i>BACK TO SITE</RouterLink>
    </header>

    <section v-if="!session" class="admin-login-wrap">
      <div class="admin-login-card">
        <div class="section-kicker">R FITNESS / ADMIN</div>
        <h1>WELCOME<br /><span>BACK.</span></h1>
        <p class="muted-copy">Sign in with the administrator credentials configured for this deployment.</p>
        <div v-if="error" class="form-feedback error-feedback mb-3">{{ error }}</div>
        <form @submit.prevent="login">
          <label class="form-label" for="admin-email">EMAIL</label>
          <input id="admin-email" v-model="email" class="form-control mb-3" type="email" autocomplete="username" required />
          <label class="form-label" for="admin-password">PASSWORD</label>
          <input id="admin-password" v-model="password" class="form-control mb-4" type="password" autocomplete="current-password" required />
          <button class="btn btn-accent w-100" type="submit" :disabled="busy">{{ busy ? 'SIGNING IN...' : 'SIGN IN' }} <i class="bi bi-arrow-right ms-2"></i></button>
        </form>
        <p class="form-note mt-3 mb-0">Admin API access uses a signed session that expires after eight hours.</p>
      </div>
    </section>

    <section v-else class="admin-content container-xl py-5">
      <div class="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-4">
        <div>
          <div class="section-kicker">R FITNESS / OVERVIEW</div>
          <h1 class="admin-title">THE <span>BACK OFFICE.</span></h1>
        </div>
        <button class="btn btn-outline-light" @click="loadDashboard" :disabled="loading"><i class="bi bi-arrow-clockwise me-2"></i>REFRESH</button>
      </div>

      <div v-if="error" class="form-feedback error-feedback mb-3">{{ error }}</div>
      <div v-if="notice" class="form-feedback success-feedback mb-3">{{ notice }}</div>

      <div class="row g-3 mb-5">
        <div class="col-md-4"><div class="admin-stat"><span>TOTAL ENQUIRIES</span><strong>{{ overview.total_leads }}</strong></div></div>
        <div class="col-md-4"><div class="admin-stat"><span>NEW ENQUIRIES</span><strong>{{ overview.new_leads }}</strong></div></div>
        <div class="col-md-4"><div class="admin-stat"><span>ACTIVE PLANS</span><strong>{{ overview.active_plans }}</strong></div></div>
      </div>

      <section class="admin-panel mb-5">
        <div class="admin-panel-heading">
          <div><div class="section-kicker">01 / FOLLOW UP</div><h2>ENQUIRIES <span>INBOX</span></h2></div>
          <span class="admin-count">{{ leads.length }} RECORDS</span>
        </div>
        <div v-if="loading" class="admin-empty">Loading enquiries…</div>
        <div v-else-if="!leads.length" class="admin-empty">No enquiries yet. New website submissions will appear here.</div>
        <div v-else class="table-responsive">
          <table class="table admin-table align-middle">
            <thead><tr><th>PERSON</th><th>CONTACT</th><th>GOAL</th><th>RECEIVED</th><th>STATUS</th></tr></thead>
            <tbody>
              <tr v-for="lead in leads" :key="lead.id">
                <td><strong>{{ lead.full_name }}</strong><small>{{ lead.email || 'No email supplied' }}</small><small v-if="lead.message">{{ lead.message }}</small></td>
                <td><a :href="`tel:${lead.phone}`">{{ lead.phone }}</a><small>{{ lead.preferred_contact }}</small></td>
                <td>{{ lead.fitness_goal || '—' }}</td>
                <td>{{ formatDate(lead.created_at) }}</td>
                <td>
                  <select class="form-select form-select-sm status-select" :value="lead.status" @change="updateStatus(lead.id, $event)">
                    <option value="new">New</option><option value="contacted">Contacted</option><option value="converted">Converted</option><option value="closed">Closed</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="admin-panel">
        <div class="admin-panel-heading">
          <div><div class="section-kicker">02 / EDIT THE OFFER</div><h2>MEMBERSHIP <span>PLANS</span></h2></div>
          <button class="btn btn-accent btn-sm" @click="showPlanForm = !showPlanForm"><i class="bi bi-plus-lg me-2"></i>ADD PLAN</button>
        </div>
        <form v-if="showPlanForm" class="admin-plan-form mb-4" @submit.prevent="createPlan">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">PLAN NAME</label><input v-model="draft.title" class="form-control" required minlength="2" maxlength="100" /></div>
            <div class="col-md-6"><label class="form-label">DURATION (DAYS)</label><input v-model="draft.duration_days" class="form-control" type="number" min="1" max="3650" placeholder="Optional" /></div>
            <div class="col-12"><label class="form-label">DESCRIPTION</label><input v-model="draft.description" class="form-control" /></div>
            <div class="col-md-6"><label class="form-label">PRICE LABEL</label><input v-model="draft.price_label" class="form-control" maxlength="80" /></div>
            <div class="col-md-6"><label class="form-label">FEATURES (ONE PER LINE)</label><textarea v-model="draft.features" class="form-control" rows="2"></textarea></div>
            <div class="col-12 d-flex gap-2"><button class="btn btn-accent" type="submit" :disabled="busy">{{ busy ? 'SAVING…' : 'SAVE PLAN' }}</button><button class="btn btn-outline-light" type="button" @click="showPlanForm = false">CANCEL</button></div>
          </div>
        </form>
        <div v-if="!plans.length" class="admin-empty">No membership plans yet. Add confirmed plans and pricing here.</div>
        <div v-else class="row g-3">
          <div v-for="plan in plans" :key="plan.id" class="col-md-6 col-xl-4">
            <article class="admin-plan-card" :class="{ inactive: !plan.is_active }">
              <div class="d-flex justify-content-between align-items-start gap-2"><span class="admin-plan-status">{{ plan.is_active ? 'LIVE ON WEBSITE' : 'HIDDEN' }}</span><button class="icon-action" :aria-label="plan.is_active ? 'Hide plan' : 'Publish plan'" @click="togglePlan(plan)"><i class="bi" :class="plan.is_active ? 'bi-eye' : 'bi-eye-slash'"></i></button></div>
              <h3>{{ plan.title }}</h3>
              <p>{{ plan.price_label }}</p>
              <small>{{ plan.duration_days ? `${plan.duration_days} days` : 'Duration not set' }}</small>
            </article>
          </div>
        </div>
      </section>
      <p class="admin-footnote mt-4">Only publish prices, timings, trainer details and programmes after they have been confirmed by gym management.</p>
    </section>
  </main>
</template>
