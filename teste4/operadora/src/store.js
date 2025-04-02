import { createStore } from 'vuex'
import api from '@/services/api'

export default createStore({
  state: {
    loading: false,
    searchResults: [],
    error: null,
    pagination: {
      currentPage: 1,
      totalPages: 0,
      totalItems: 0,
      itemsPerPage: 10
    }
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_SEARCH_RESULTS(state, { results, pagination }) {
      state.searchResults = results
      state.pagination = {
        currentPage: pagination.current_page,
        totalPages: pagination.total_pages,
        totalItems: pagination.total_items,
        itemsPerPage: pagination.per_page
      }
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    async searchOperadoras({ commit }, { query, page = 1, limit = 10 }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const response = await api.get('/search', {
          params: { 
            q: query,
            page,
            limit,
            field: 'Nome_Fantasia'
          }
        })
        
        commit('SET_SEARCH_RESULTS', {
          results: response.data.results,
          pagination: response.data.pagination
        })
      } catch (error) {
        commit('SET_ERROR', error)
        commit('SET_SEARCH_RESULTS', { results: [], pagination: {} })
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
})