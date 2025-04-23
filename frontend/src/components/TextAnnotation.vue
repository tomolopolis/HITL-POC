<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

interface TextItem {
  id: number
  text: string
  label: string | null
  created_at: string
  project: number
}

const exampleData: TextItem[] = [
  {
    id: 1,
    text: "The quick brown fox jumps over the lazy dog.",
    label: 'Foo',
    created_at: new Date().toISOString(),
    project: 1
  },
  {
    id: 2,
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    label: 'Bar',
    created_at: new Date().toISOString(),
    project: 1
  },
  {
    id: 3,
    text: "To be or not to be, that is the question.",
    label: 'Baz',
    created_at: new Date().toISOString(),
    project: 1
  },
  {
    id: 4,
    text: "In a hole in the ground there lived a hobbit.",
    label: null,
    created_at: new Date().toISOString(),
    project: 1
  },
  {
    id: 5,
    text: "It was the best of times, it was the worst of times.",
    label: null,
    created_at: new Date().toISOString(),
    project: 1
  }
]

export default defineComponent({
  name: 'TextAnnotation',
  props: {
    projectId: {
      type: Number,
      required: true
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      items: [] as TextItem[],
      currentIndex: 0,
      loading: true
    }
  },
  computed: {
    progress(): number {
      return Math.round((this.currentIndex / this.items.length) * 100)
    },
    isComplete(): boolean {
      return this.currentIndex >= this.items.length
    }
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get(`http://localhost:8001/api/items/?project=${this.projectId}`)
        this.items = response.data
        this.loading = false
      } catch (error) {
        console.error('Error fetching items:', error)
        // Use example data when API call fails
        this.items = exampleData.map(item => ({
          ...item,
          project: this.projectId
        }))
        this.loading = false
      }
    },
    async labelText(label: 'Correct' | 'Incorrect') {
      if (this.currentIndex < this.items.length) {
        const item = this.items[this.currentIndex]
        try {
          await axios.patch(`http://localhost:8001/api/items/${item.id}/`, {
            label: label
          })
          this.items[this.currentIndex].label = label
          this.currentIndex++
        } catch (error) {
          console.error('Error updating label:', error)
          // Update local state even if API call fails
          this.items[this.currentIndex].label = label
          this.currentIndex++
        }
      }
    },
    goBack() {
      this.router.push('/home')
    }
  },
  mounted() {
    this.fetchItems()
  }
})
</script>

<template>
  <div class="annotation-container">
    <button class="back-btn" @click="goBack">← Back to Projects</button>
    <h1>Text Annotation Tool</h1>
    
    <div v-if="loading" class="loading">
      Loading items...
    </div>
    
    <div v-else-if="!isComplete" class="content">
      <div class="progress-bar">
        <div class="progress" :style="{ width: `${progress}%` }"></div>
      </div>
      
      <div class="text-display">
        <p>{{ items[currentIndex].text }}</p>
      </div>
      
      <div class="button-container">
        <button 
          class="correct-btn"
          @click="labelText('Correct')"
        >
          Correct
        </button>
        <button 
          class="incorrect-btn"
          @click="labelText('Incorrect')"
        >
          Incorrect
        </button>
      </div>
    </div>

    <div v-else class="complete">
      <h2>Annotation Complete!</h2>
      <div class="results">
        <h3>Results:</h3>
        <ul>
          <li v-for="item in items" :key="item.id">
            <span class="text">{{ item.text }}</span>
            <span :class="['label', item.label?.toLowerCase()]">{{ item.label }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.annotation-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

.back-btn {
  background-color: transparent;
  border: 1px solid #646cff;
  color: #646cff;
  margin-bottom: 1rem;
}

.back-btn:hover {
  background-color: #646cff;
  color: white;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #2c2c2c;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #646cff;
  transition: width 0.3s ease;
}

.text-display {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.text-display p {
  font-size: 1.2rem;
  margin: 0;
}

.button-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

button {
  min-width: 120px;
}

.correct-btn {
  background-color: #22c55e;
}

.incorrect-btn {
  background-color: #ef4444;
}

.correct-btn:hover {
  border-color: #16a34a;
}

.incorrect-btn:hover {
  border-color: #dc2626;
}

.complete {
  text-align: center;
}

.results {
  margin-top: 2rem;
  text-align: left;
}

.results ul {
  list-style: none;
  padding: 0;
}

.results li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  margin: 0.5rem 0;
  background-color: #1a1a1a;
  border-radius: 4px;
}

.label {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.label.correct {
  background-color: #22c55e;
}

.label.incorrect {
  background-color: #ef4444;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #646cff;
}
</style>