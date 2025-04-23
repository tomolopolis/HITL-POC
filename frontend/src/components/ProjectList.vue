<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

interface Project {
  id: number
  name: string
  description: string
  created_at: string
}

export default defineComponent({
  name: 'ProjectList',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      projects: [] as Project[],
      loading: true
    }
  },
  methods: {
    async fetchProjects() {
      try {
        const response = await axios.get('http://localhost:8001/api/projects/')
        this.projects = response.data
        this.loading = false
      } catch (error) {
        console.error('Error fetching projects:', error)
        this.loading = false
      }
    },
    handleProjectSelect(projectId: number) {
      this.router.push(`/annotations/${projectId}`)
    }
  },
  mounted() {
    this.fetchProjects()
  }
})
</script>

<template>
  <div class="projects-container">
    <h1>Annotation Projects</h1>
    
    <div v-if="loading" class="loading">
      Loading projects...
    </div>
    
    <div v-else class="projects-list">
      <div 
        v-for="project in projects" 
        :key="project.id"
        class="project-card"
        @click="handleProjectSelect(project.id)"
      >
        <h2>{{ project.name }}</h2>
        <p>{{ project.description }}</p>
        <span class="created-at">Created: {{ new Date(project.created_at).toLocaleDateString() }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.projects-container {
  max-width: 800px;
  margin: 0 auto;
}

.projects-list {
  display: grid;
  gap: 1rem;
  margin-top: 2rem;
}

.project-card {
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.project-card:hover {
  transform: translateY(-2px);
}

.project-card h2 {
  margin: 0 0 0.5rem 0;
  color: #646cff;
}

.project-card p {
  margin: 0 0 1rem 0;
  color: rgba(255, 255, 255, 0.7);
}

.created-at {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #646cff;
  margin-top: 2rem;
}
</style>