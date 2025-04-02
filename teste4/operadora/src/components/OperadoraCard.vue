<template>
  <div class="card" :class="{ 'expanded': showDetails }" @click="toggleDetails">
    <!-- Header da Card -->
    <div class="card-header">
      <div class="corporate-brand">
        <div class="ans-badge">ANS {{ operadora.Registro_ANS || 'N/A' }}</div>
        <h3 class="company-name">{{ operadora.Nome_Fantasia || 'Operadora de Saúde' }}</h3>
        <div class="corporate-info">
          <span class="corporate-type">{{ operadora.Modalidade || 'Modalidade não informada' }}</span>
          <span class="region">{{ operadora.Regiao_de_Comercializacao || 'Região não especificada' }}</span>
        </div>
      </div>
      <div class="quick-info">
        <div class="info-item">
          <svg class="icon" viewBox="0 0 24 24">
            <path d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"/>
          </svg>
          <div>
            <div class="info-label">Localização</div>
            <div class="info-value">{{ operadora.Cidade || 'Cidade não informada' }}/{{ operadora.UF || 'UF não informada' }}</div>
          </div>
        </div>
        <div class="info-item">
          <svg class="icon" viewBox="0 0 24 24">
            <path d="M6.62,10.79C8.06,13.62 10.38,15.94 13.21,17.38L15.41,15.18C15.69,14.9 16.08,14.82 16.43,14.93C17.55,15.3 18.75,15.5 20,15.5A1,1 0 0,1 21,16.5V20A1,1 0 0,1 20,21A17,17 0 0,1 3,4A1,1 0 0,1 4,3H7.5A1,1 0 0,1 8.5,4C8.5,5.25 8.7,6.45 9.07,7.57C9.18,7.92 9.1,8.31 8.82,8.59L6.62,10.79Z"/>
          </svg>
          <div>
            <div class="info-label">Contato</div>
            <div class="info-value">{{ formatPhone(operadora.DDD, operadora.Telefone) || 'Não disponível' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detalhes Expandidos -->
    <transition name="expand">
      <div v-show="showDetails" class="card-details">
        <!-- Dados Corporativos -->
        <div class="detail-section">
          <h4 class="section-title">
            <svg class="section-icon" viewBox="0 0 24 24">
              <path d="M12,15C12.81,15 13.5,14.7 14.11,14.11C14.7,13.5 15,12.81 15,12C15,11.19 14.7,10.5 14.11,9.89C13.5,9.3 12.81,9 12,9C11.19,9 10.5,9.3 9.89,9.89C9.3,10.5 9,11.19 9,12C9,12.81 9.3,13.5 9.89,14.11C10.5,14.7 11.19,15 12,15M12,2C14.75,2 17.1,3 19.05,4.95C21,6.9 22,9.25 22,12V13.45C22,14.45 21.65,15.3 21,16C20.3,16.67 19.5,17 18.5,17C17.3,17 16.31,16.5 15.56,15.5C14.56,16.5 13.38,17 12,17C10.63,17 9.45,16.5 8.46,15.54C7.5,14.55 7,13.38 7,12C7,10.63 7.5,9.45 8.46,8.46C9.45,7.5 10.63,7 12,7C13.38,7 14.55,7.5 15.54,8.46C16.5,9.45 17,10.63 17,12V13.45C17,14.15 17.17,14.75 17.46,15.29C17.75,15.83 18.15,16.25 18.65,16.56C19.13,16.87 19.7,17 20.36,17C20.87,17 21.3,16.83 21.7,16.5C22.06,16.13 22.24,15.7 22.24,15.19L22.24,12C22.24,8.15 20.88,5.11 18.18,3.41C16.17,2.28 14.13,1.75 12.06,1.75L12,2M3.28,4.28L2,5.5L4.04,7.5L5.5,6.04L3.28,4.28M19.96,16.5L21.28,17.84L19.84,19.16L18.5,17.84L19.96,16.5M12,20V22C10.25,22 8.58,21.72 7,21.19L7.39,19.44C8.5,19.8 9.7,20 11,20H12M4,11H2V13H4V11M22,11H20V13H22V11M12,4V6C13.38,6 14.63,6.2 15.75,6.55L15.26,8.31C14.5,8.09 13.78,7.95 13.05,7.87L12.71,7.83L12.37,7.8C12.13,7.77 11.88,7.75 11.62,7.75H11.57C11.25,7.75 10.94,7.77 10.64,7.8C10.34,7.83 10.07,7.87 9.82,7.92L9.19,8.05L8.57,8.22C8.07,8.38 7.6,8.57 7.15,8.8L6.62,8.31C7.93,7.5 9.43,7 11,7H12V4Z"/>
            </svg>
            Dados Corporativos
          </h4>
          <div class="detail-grid">
            <div class="detail-item">
              <label>Razão Social</label>
              <div>{{ operadora.Razao_Social || 'Não informada' }}</div>
            </div>
            <div class="detail-item">
              <label>CNPJ</label>
              <div>{{ formatCNPJ(operadora.CNPJ) || 'Não informado' }}</div>
            </div>
            <div class="detail-item">
              <label>Data de Registro</label>
              <div>{{ formatDate(operadora.Data_Registro_ANS) }}</div>
            </div>
          </div>
        </div>

        <!-- Endereço Completo -->
        <div class="detail-section">
          <h4 class="section-title">
            <svg class="section-icon" viewBox="0 0 24 24">
              <path d="M12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5M12,2A7,7 0 0,1 19,9C19,14.25 12,22 12,22C12,22 5,14.25 5,9A7,7 0 0,1 12,2M12,4A5,5 0 0,0 7,9C7,10 7,12 12,18.71C17,12 17,10 17,9A5,5 0 0,0 12,4Z"/>
            </svg>
            Endereço Completo
          </h4>
          <div class="address-box">
            <div class="address-line">
              {{ operadora.Logradouro || 'Endereço não informado' }} {{ operadora.Numero }}
            </div>
            <div class="address-line" v-if="operadora.Complemento">
              Complemento: {{ operadora.Complemento }}
            </div>
            <div class="address-line">
              {{ operadora.Bairro || 'Bairro não informado' }} • {{ operadora.CEP ? formatCEP(operadora.CEP) : 'CEP não informado' }}
            </div>
          </div>
        </div>

        <!-- Contatos -->
        <div class="detail-section" v-if="operadora.Endereco_eletronico || operadora.Fax || operadora.Representante">
          <h4 class="section-title">
            <svg class="section-icon" viewBox="0 0 24 24">
              <path d="M12,7.5A4.5,4.5 0 0,1 16.5,12A4.5,4.5 0 0,1 12,16.5A4.5,4.5 0 0,1 7.5,12A4.5,4.5 0 0,1 12,7.5M12,5A6.5,6.5 0 0,0 5,12C5,14.25 12,21 12,21C12,21 19,14.25 19,12A6.5,6.5 0 0,0 12,5Z"/>
            </svg>
            Contatos
          </h4>
          <div class="contact-box">
            <div v-if="operadora.Endereco_eletronico">
              <label>Email:</label>
              <div>{{ operadora.Endereco_eletronico }}</div>
            </div>
            <div v-if="operadora.Fax">
              <label>Fax:</label>
              <div>{{ formatFax(operadora.Fax) }}</div>
            </div>
            <div v-if="operadora.Representante">
              <label>Representante:</label>
              <div>{{ operadora.Representante }}</div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    operadora: Object
  },
  data() {
    return {
      showDetails: false
    };
  },
  methods: {
    toggleDetails() {
      this.showDetails = !this.showDetails;
    },
    formatPhone(ddd, phone) {
      return ddd && phone ? `(${ddd}) ${phone}` : '';
    },
    formatCNPJ(cnpj) {
      return cnpj ? cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5') : '';
    },
    formatDate(date) {
      return date ? new Date(date).toLocaleDateString() : 'Data não disponível';
    },
    formatCEP(cep) {
      return cep ? cep.replace(/(\d{5})(\d{3})/, '$1-$2') : 'CEP não informado';
    },
    formatFax(fax) {
      return fax ? `Fax: ${fax}` : 'Fax não disponível';
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.card {
  background: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 32, 63, 0.08);
  margin-bottom: 20px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid #F0F4F8;
  font-family: 'Inter', sans-serif;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 32, 63, 0.12);
}

.card-header {
  padding: 24px;
  background: linear-gradient(135deg, #F8FAFC 0%, #F0F4F8 100%);
}

.ans-badge {
  display: inline-block;
  background: #3B82F6;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.company-name {
  color: #1E293B;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.corporate-info {
  display: flex;
  gap: 12px;
  font-size: 0.875rem;
  color: #64748B;
}

.quick-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-top: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.icon {
  width: 24px;
  height: 24px;
  fill: #3B82F6;
  flex-shrink: 0;
}

.info-label {
  color: #64748B;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 4px;
}

.info-value {
  color: #1E293B;
  font-weight: 600;
  line-height: 1.4;
}

.card-details {
  padding: 24px;
  background: #FFFFFF;
  border-top: 1px solid #F1F5F9;
}

.detail-section {
  margin-bottom: 32px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #1E293B;
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0 0 20px 0;
}

.section-icon {
  width: 24px;
  height: 24px;
  fill: #3B82F6;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.detail-item {
  background: #F8FAFC;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #3B82F6;
}

.detail-item label {
  display: block;
  color: #64748B;
  font-size: 0.875rem;
  margin-bottom: 8px;
}

.address-box {
  background: #F8FAFC;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.address-line {
  color: #475569;
  line-height: 1.6;
  margin-bottom: 8px;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.contact-item {
  padding: 16px;
  background: #F8FAFC;
  border-radius: 8px;
  border-left: 4px solid #3B82F6;
}

.contact-type {
  color: #64748B;
  font-size: 0.875rem;
  margin-bottom: 8px;
}

.contact-value {
  color: #1E293B;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.contact-value:hover {
  color: #3B82F6;
}

.contact-sub {
  color: #64748B;
  font-size: 0.875rem;
  margin-top: 8px;
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}

.expand-enter-to,
.expand-leave-from {
  max-height: 1000px;
  opacity: 1;
}

@media (max-width: 768px) {
  .card-header {
    padding: 20px;
  }
  
  .company-name {
    font-size: 1.25rem;
  }
  
  .quick-info {
    grid-template-columns: 1fr;
  }
  
  .info-item {
    padding: 12px;
  }
  
  .detail-grid,
  .contact-grid {
    grid-template-columns: 1fr;
  }
}
</style>