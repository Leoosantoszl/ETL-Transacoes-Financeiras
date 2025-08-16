variable "location" {
  description = "Região da Azure para criar os recursos"
  type        = string
  default     = "East US"
}

variable "admin_username" {
  description = "Nome do usuário administrador"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "Caminho para a chave pública SSH"
  type        = string
}

variable "repo_url" {
  description = "URL do repositório Git do projeto"
  default     = "https://github.com/Leoosantoszl/ETL-Transacoes-Financeiras.git"
  type        = string
}
