<template>
  <div class="home">
    <div class="search-container">
      <h1>Busca de Operadoras</h1>
      <div class="search-box">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Digite o nome fantasia da operadora..."
          @input="onSearchInput"
          @keyup.esc="clearSearch" 
        />
        <span class="search-hint">Busque pelo nome fantasia da operadora de saúde</span>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-if="error" class="error">
      Ocorreu um erro: {{ error.message }}
    </div>

    <div v-if="!loading && searchQuery && totalItems > 0" class="pagination-controls">
      <button 
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
      >
        Anterior
      </button>
      
      <span>Página {{ currentPage }} de {{ totalPages }}</span>
      
      <button 
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
      >
        Próxima
      </button>
    </div>

    <div class="results">
      <OperadoraCard
        v-for="operadora in searchResults"
        :key="operadora.Registro_ANS"
        :operadora="operadora"
      />
    </div>


    <div v-if="!loading && searchQuery && !totalResults" class="empty">
      Nenhuma operadora encontrada com o nome fantasia "{{ searchQuery }}"
    </div>

  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import OperadoraCard from '@/components/OperadoraCard.vue'

export default {
  name: 'HomeView',
  components: { OperadoraCard },
  data() {
    return {
      searchQuery: '',
      timeout: null
    }
  },
  computed: {
    ...mapState(['loading', 'searchResults', 'error']),
    ...mapGetters(['hasResults']),
    currentPage() {
      return this.$store.state.pagination.currentPage
    },
    totalPages() {
      return this.$store.state.pagination.totalPages
    },
    totalItems() {
      return this.$store.state.pagination.totalItems
    }
  },
  methods: {
    ...mapActions(['searchOperadoras']),
    onSearchInput() {
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        if (this.searchQuery.trim()) {
          this.searchOperadoras({ 
            query: this.searchQuery.trim(),
            page: 1 // Sempre volta para a primeira página em nova busca
          })
        }
      }, 500)
    },
    changePage(newPage) {
      if (newPage >= 1 && newPage <= this.totalPages) {
        this.searchOperadoras({
          query: this.searchQuery.trim(),
          page: newPage
        })
      }
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-container {
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  max-width: 600px;
}

.search-box input {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
}

.search-hint {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.5rem;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.results-info {
  margin: 1rem 0;
  font-weight: 500;
  color: #64748b;
}

.error, .empty {
  padding: 2rem;
  text-align: center;
  color: #ef4444;
}

.empty {
  color: #64748b;
}

.search-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  font-size: 0.875rem;
  color: #64748B;
}


.search-box {
  position: relative;
}

.search-info svg {
  flex-shrink: 0;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
}

.pagination-controls button {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.pagination-controls button:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

.pagination-controls button:disabled {
  background-color: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
  opacity: 0.8;
}

.pagination-controls span {
  color: #64748b;
  font-size: 0.95rem;
  min-width: 120px;
  text-align: center;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }
  
  .results {
    grid-template-columns: 1fr;
  }
}
</style>