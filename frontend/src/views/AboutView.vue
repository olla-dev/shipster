<template>
  <div class="about">
    <div class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h1 class="title is-size-1">About Shipster</h1>
        </div>
      </div>
    </div>
    <div class="columns is-centered mt-5">
      <div class="column is-one-fifth  has-text-centered">
        <img src="@/assets/logo.png" alt="" class="img-fluid profile-img mt-5 mb-2" />
        <div class="columns is-centered">
            <div class="column is-half">
                <button class="button mr-2" @click="gotoGithub()">
                  <span class="icon">
                    <i class="fab fa-github"></i>
                  </span>
                </button>
                <button class="button mr-2" @click="gotoBlog()">
                  <span class="icon">
                    <i class="fa fa-globe"></i>
                  </span>
                </button>
                <button class="button" @click="gotoWebsite()">
                  <span class="icon">
                    <i class="fa fa-house"></i>
                  </span>
                </button>
            </div>
        </div>
        <span class="tag is-light">{{ year }} © Hamza Abdelkebir</span>
      </div>
      <div class="column is-one-third ml-5">
        <div class="has-text-centered">
            <div class="card-content">
              <div class="content">
                <p class="is-size-4">
                  Shipster is a platform where you can track vessel journeys. 
                </p>
                <p class="is-size-4">
                  Built with ease of use in mind with the help of:
                  <TechStack />
                </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import TechStack from '../components/TechStack.vue'
export default {
  name: 'AboutView',
  components: {
    TechStack
  },
  data() {
    return {
      year: new Date().getFullYear().toString()
    }
  },
  methods: {
    gotoGithub() {
      window.open("https://github.com/olla-dev/");
    },
    gotoBlog() {
      window.open("https://blog.codeplumbers.eu");
    },
    gotoWebsite() {
      window.open("https://codeplumbers.eu");
    }
  }
}
</script>

<style lang="scss" scoped>
  .org-description {
    margin-top: 50px;
  }
  .profile-img {
    border-radius: 50%;
  }
</style>