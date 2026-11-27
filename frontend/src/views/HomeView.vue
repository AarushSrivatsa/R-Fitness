<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SiteHeader from '../components/SiteHeader.vue'
import SiteFooter from '../components/SiteFooter.vue'
import LeadForm from '../components/LeadForm.vue'
import { apiRequest } from '../lib/api'

type Plan = {
  id: number
  title: string
  description: string | null
  duration_days: number | null
  price_amount: string | number | null
  price_label: string
  features: string[]
}

const plans = ref<Plan[]>([])
const plansLoaded = ref(false)
const phoneDisplay = '+91 73961 30212'
const phoneHref = 'tel:+917396130212'
const whatsappHref = 'https://wa.me/917396130212'

onMounted(async () => {
  try {
    plans.value = await apiRequest<Plan[]>('/api/v1/public/plans')
  } catch {
    // The website remains browsable while the API/database is being configured.
  } finally {
    plansLoaded.value = true
  }
})

function formatPrice(value: string | number | null): string {
  if (value === null || value === undefined) return ''
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(Number(value))
}
</script>

<template>
  <SiteHeader />

  <main>
    <section class="hero-section">
      <div class="hero-image"></div>
      <div class="container-xl hero-content">
        <div class="hero-eyebrow"><span class="eyebrow-line"></span> R FITNESS · UPPAL, HYDERABAD</div>
        <h1>BUILT<br />BY <span>DISCIPLINE.</span></h1>
        <p class="hero-description">Your next chapter starts with one decision.<br class="d-none d-md-block" /> Show up. Put in the work. Get stronger.</p>
        <div class="hero-actions">
          <a class="btn btn-accent btn-lg" href="#enquire">START YOUR JOURNEY <i class="bi bi-arrow-up-right ms-2"></i></a>
          <a class="btn btn-outline-light btn-lg hero-secondary" href="#about">EXPLORE THE GYM <i class="bi bi-arrow-down ms-2"></i></a>
        </div>
        <div class="hero-bottomline">
          <span><i class="bi bi-geo-alt-fill me-2"></i>UPPAL, HYDERABAD</span>
          <span class="hero-bottom-right">NO SHORTCUTS. JUST WORK.</span>
        </div>
      </div>
      <div class="hero-side-label" aria-hidden="true">STRENGTH · FOCUS · PROGRESS</div>
    </section>

    <section id="about" class="section-pad about-section">
      <div class="container-xl">
        <div class="row align-items-end g-5">
          <div class="col-lg-6">
            <div class="section-kicker">01 / THE MINDSET</div>
            <h2 class="section-title">MORE THAN<br />A <span>WORKOUT.</span></h2>
          </div>
          <div class="col-lg-5 offset-lg-1">
            <p class="large-copy">A stronger version of you is built one session at a time.</p>
            <p class="muted-copy">Whether you are getting started or pushing for your next personal best, make the commitment and take the first step. The R Fitness team is here to help you explore the right way to train.</p>
            <a class="text-link" href="#enquire">LET'S GET YOU STARTED <i class="bi bi-arrow-up-right"></i></a>
          </div>
        </div>

        <div class="about-strip row g-0 mt-5">
          <div class="col-6 col-lg-3 about-stat">
            <span class="stat-symbol">01</span><span class="stat-label">SHOW UP</span>
          </div>
          <div class="col-6 col-lg-3 about-stat">
            <span class="stat-symbol">02</span><span class="stat-label">STAY CONSISTENT</span>
          </div>
          <div class="col-6 col-lg-3 about-stat">
            <span class="stat-symbol">03</span><span class="stat-label">KEEP LEARNING</span>
          </div>
          <div class="col-6 col-lg-3 about-stat">
            <span class="stat-symbol">04</span><span class="stat-label">GET STRONGER</span>
          </div>
        </div>
      </div>
    </section>

    <section id="training" class="section-pad training-section">
      <div class="container-xl">
        <div class="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-5">
          <div>
            <div class="section-kicker">02 / FIND YOUR FOCUS</div>
            <h2 class="section-title mb-0">MAKE EVERY<br /><span>REP COUNT.</span></h2>
          </div>
          <p class="muted-copy training-intro mb-1">Start with your goal. Build a routine. Keep moving forward.</p>
        </div>
        <div class="row g-3">
          <div class="col-md-4">
            <article class="training-card training-card-one">
              <span class="card-index">01</span>
              <div class="training-card-content">
                <i class="bi bi-lightning-charge-fill"></i>
                <h3>STRENGTH<br />& CONDITIONING</h3>
                <p>Build a solid foundation with focused, progressive training.</p>
              </div>
            </article>
          </div>
          <div class="col-md-4">
            <article class="training-card training-card-two">
              <span class="card-index">02</span>
              <div class="training-card-content">
                <i class="bi bi-bullseye"></i>
                <h3>PERSONAL<br />COACHING</h3>
                <p>Ask about guidance that matches your experience and goals.</p>
              </div>
            </article>
          </div>
          <div class="col-md-4">
            <article class="training-card training-card-three">
              <span class="card-index">03</span>
              <div class="training-card-content">
                <i class="bi bi-activity"></i>
                <h3>FITNESS<br />& CONDITIONING</h3>
                <p>Work on stamina, consistency and all-round fitness.</p>
              </div>
            </article>
          </div>
        </div>
        <p class="fine-print mt-3">Training options and coach availability can vary. Contact the gym for the current programme and schedule.</p>
      </div>
    </section>

    <section class="statement-band">
      <div class="container-xl">
        <p>THE ONLY BAD WORKOUT<br />IS THE ONE <span>YOU SKIP.</span></p>
      </div>
    </section>

    <section id="membership" class="section-pad membership-section">
      <div class="container-xl">
        <div class="row align-items-end g-4 mb-5">
          <div class="col-lg-7">
            <div class="section-kicker">03 / YOUR NEXT MOVE</div>
            <h2 class="section-title mb-0">FIND YOUR<br /><span>COMMITMENT.</span></h2>
          </div>
          <div class="col-lg-4 offset-lg-1">
            <p class="muted-copy mb-0">The right plan starts with a conversation. Ask the team about current membership options, inclusions and pricing.</p>
          </div>
        </div>

        <div v-if="plans.length" class="row g-3">
          <div v-for="plan in plans" :key="plan.id" class="col-md-6 col-lg-4">
            <article class="plan-card h-100">
              <div class="plan-topline"><span>R FITNESS MEMBERSHIP</span><i class="bi bi-arrow-up-right"></i></div>
              <h3>{{ plan.title }}</h3>
              <p class="muted-copy">{{ plan.description || 'Speak with the team to find the right fit.' }}</p>
              <div class="plan-price">{{ formatPrice(plan.price_amount) || plan.price_label }}</div>
              <ul v-if="plan.features?.length" class="plan-features">
                <li v-for="feature in plan.features" :key="feature"><i class="bi bi-check2"></i>{{ feature }}</li>
              </ul>
              <a class="btn btn-outline-light w-100 mt-auto" href="#enquire">ENQUIRE ABOUT THIS PLAN <i class="bi bi-arrow-up-right ms-2"></i></a>
            </article>
          </div>
        </div>
        <div v-else class="membership-enquire-card">
          <div>
            <div class="section-kicker">MEMBERSHIP OPTIONS</div>
            <h3>YOUR GOALS.<br /><span>YOUR GAME PLAN.</span></h3>
            <p class="muted-copy mb-0">Contact R Fitness for current plans, pricing and membership details.</p>
          </div>
          <a class="btn btn-accent btn-lg" href="#enquire">ASK ABOUT MEMBERSHIP <i class="bi bi-arrow-up-right ms-2"></i></a>
        </div>
        <p v-if="!plansLoaded" class="fine-print mt-3">Loading current membership options…</p>
      </div>
    </section>

    <section class="gallery-section">
      <div class="gallery-grid">
        <div class="gallery-tile gallery-wide">
          <img src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1400&q=85" alt="Gym training floor with strength equipment" loading="lazy" />
        </div>
        <div class="gallery-tile">
          <img src="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=900&q=85" alt="Athlete training with weights" loading="lazy" />
        </div>
        <div class="gallery-tile">
          <img src="https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=900&q=85" alt="Training session in a gym" loading="lazy" />
        </div>
      </div>
      <div class="gallery-caption container-xl">
        <span>YOUR WORK. YOUR PACE. YOUR PROGRESS.</span>
        <span class="fine-print">Representative fitness photography — replace with original R Fitness photos before launch.</span>
      </div>
    </section>

    <section id="location" class="section-pad location-section">
      <div class="container-xl">
        <div class="section-kicker">04 / COME THROUGH</div>
        <div class="row g-5 mt-1">
          <div class="col-lg-6">
            <h2 class="section-title">YOUR NEXT<br /><span>SESSION AWAITS.</span></h2>
            <p class="muted-copy location-copy">Find R Fitness in Uppal. Reach out before visiting to confirm the latest opening hours and training availability.</p>
            <div class="contact-detail">
              <i class="bi bi-geo-alt"></i>
              <div><span>ADDRESS</span><p>3rd Floor, Jetta Mallaiah Complex, Uppal Road, near Gandhi Statue, Vijayapuri Colony, Uppal, Hyderabad, Telangana 500039.</p></div>
            </div>
            <div class="contact-detail">
              <i class="bi bi-telephone"></i>
              <div><span>CALL THE GYM</span><a :href="phoneHref">{{ phoneDisplay }}</a></div>
            </div>
            <div class="contact-detail">
              <i class="bi bi-clock"></i>
              <div><span>OPENING HOURS</span><p>Contact the gym for current opening hours and class timings.</p></div>
            </div>
            <div class="d-flex flex-wrap gap-3 mt-4">
              <a class="btn btn-accent" href="https://www.google.com/maps/search/?api=1&query=R+Fitness+Jetta+Mallaiah+Complex+Uppal+Hyderabad" target="_blank" rel="noreferrer">GET DIRECTIONS <i class="bi bi-arrow-up-right ms-2"></i></a>
              <a class="btn btn-outline-light" href="https://www.instagram.com/rfitness_gym/" target="_blank" rel="noreferrer">INSTAGRAM <i class="bi bi-instagram ms-2"></i></a>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="location-visual">
              <div class="location-visual-inner">
                <div class="location-pin"><i class="bi bi-geo-alt-fill"></i></div>
                <span>R FITNESS</span>
                <strong>UPPAL<br />HYDERABAD</strong>
                <small>3RD FLOOR · JETTA MALLAIAH COMPLEX</small>
                <a href="https://www.google.com/maps/search/?api=1&query=R+Fitness+Uppal+Hyderabad" target="_blank" rel="noreferrer">OPEN IN MAPS <i class="bi bi-arrow-up-right"></i></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="enquire" class="section-pad enquiry-section">
      <div class="container-xl">
        <div class="row g-5">
          <div class="col-lg-5">
            <div class="section-kicker">05 / TAKE THE FIRST STEP</div>
            <h2 class="section-title">LET'S GET<br /><span>TO WORK.</span></h2>
            <p class="muted-copy enquiry-copy">Tell us what you are working towards. Leave your details and the team can get back to you.</p>
            <a class="whatsapp-link" :href="whatsappHref" target="_blank" rel="noreferrer"><i class="bi bi-whatsapp"></i><span>Prefer WhatsApp?<small>Message R Fitness directly</small></span><i class="bi bi-arrow-up-right ms-auto"></i></a>
          </div>
          <div class="col-lg-7">
            <LeadForm />
          </div>
        </div>
      </div>
    </section>
  </main>

  <SiteFooter />
</template>
