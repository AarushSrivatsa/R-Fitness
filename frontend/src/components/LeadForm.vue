<script setup lang="ts">
import { reactive, ref } from 'vue'
import { apiRequest } from '../lib/api'

const form = reactive({
  full_name: '',
  phone: '',
  email: '',
  fitness_goal: '',
  preferred_contact: 'whatsapp',
  message: '',
})
const busy = ref(false)
const success = ref(false)
const error = ref('')

async function submit() {
  busy.value = true
  success.value = false
  error.value = ''
  try {
    await apiRequest('/api/v1/leads', {
      method: 'POST',
      body: JSON.stringify({
        ...form,
        email: form.email.trim() || null,
        fitness_goal: form.fitness_goal || null,
        message: form.message.trim() || null,
      }),
    })
    success.value = true
    Object.assign(form, {
      full_name: '', phone: '', email: '', fitness_goal: '',
      preferred_contact: 'whatsapp', message: '',
    })
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not send your enquiry. Please call us instead.'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <form class="lead-form" @submit.prevent="submit">
    <div v-if="success" class="form-feedback success-feedback" role="status">
      <i class="bi bi-check-circle-fill me-2"></i>
      Enquiry received. The R Fitness team can follow up with you soon.
    </div>
    <div v-if="error" class="form-feedback error-feedback" role="alert">{{ error }}</div>

    <div class="row g-3">
      <div class="col-md-6">
        <label class="form-label" for="lead-name">YOUR NAME</label>
        <input id="lead-name" v-model="form.full_name" class="form-control" autocomplete="name" placeholder="Enter your name" minlength="2" maxlength="120" required />
      </div>
      <div class="col-md-6">
        <label class="form-label" for="lead-phone">PHONE NUMBER</label>
        <input id="lead-phone" v-model="form.phone" class="form-control" type="tel" autocomplete="tel" placeholder="+91 00000 00000" minlength="7" maxlength="32" required />
      </div>
      <div class="col-md-6">
        <label class="form-label" for="lead-email">EMAIL <span class="optional-label">OPTIONAL</span></label>
        <input id="lead-email" v-model="form.email" class="form-control" type="email" autocomplete="email" placeholder="you@example.com" maxlength="254" />
      </div>
      <div class="col-md-6">
        <label class="form-label" for="lead-goal">YOUR FITNESS GOAL</label>
        <select id="lead-goal" v-model="form.fitness_goal" class="form-select">
          <option value="">Choose a goal</option>
          <option>Build strength</option>
          <option>Lose weight</option>
          <option>Improve fitness</option>
          <option>Build muscle</option>
          <option>Just getting started</option>
          <option>Something else</option>
        </select>
      </div>
      <div class="col-12">
        <label class="form-label" for="lead-contact">PREFERRED WAY TO CONTACT YOU</label>
        <select id="lead-contact" v-model="form.preferred_contact" class="form-select">
          <option value="whatsapp">WhatsApp</option>
          <option value="phone">Phone call</option>
          <option value="email">Email</option>
        </select>
      </div>
      <div class="col-12">
        <label class="form-label" for="lead-message">ANYTHING ELSE? <span class="optional-label">OPTIONAL</span></label>
        <textarea id="lead-message" v-model="form.message" class="form-control" rows="3" maxlength="2000" placeholder="Tell us what you want to work towards..."></textarea>
      </div>
      <div class="col-12">
        <button class="btn btn-accent w-100 submit-btn" type="submit" :disabled="busy">
          {{ busy ? 'SENDING...' : 'SEND MY ENQUIRY' }}
          <i class="bi bi-arrow-up-right ms-2"></i>
        </button>
        <p class="form-note mt-3 mb-0">By submitting, you agree that the gym may contact you about your enquiry.</p>
      </div>
    </div>
  </form>
</template>
