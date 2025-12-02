"""
Cliente para API do SABIA-3.1 da Maritaca

Substitui o uso do modelo base SABIA-7B local pela API.
"""

import os
import requests
import json
from pathlib import Path
from typing import List, Dict, Optional

# Função para carregar .env
def _load_env_file():
    """Carrega variáveis do arquivo .env"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            # Se python-dotenv não estiver instalado, carrega manualmente
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

# Carregar .env na importação
_load_env_file()


class MaritacaAPI:
    """Cliente para API do SABIA-3.1 da Maritaca."""
    
    BASE_URL = "https://chat.maritaca.ai/api/chat/completions"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o cliente da API.
        
        Args:
            api_key: Chave da API. Se None, tenta ler de MARITACA_API_KEY env var ou .env file.
        """
        # Primeiro tenta usar a chave fornecida
        if api_key:
            self.api_key = str(api_key).strip()
        else:
            # Tenta ler da variável de ambiente (já carregada do .env se existir)
            self.api_key = os.getenv("MARITACA_API_KEY")
            if self.api_key:
                self.api_key = str(self.api_key).strip()
            
            # Se ainda não encontrou, tenta carregar .env manualmente
            if not self.api_key:
                env_path = Path(__file__).parent / '.env'
                if env_path.exists():
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                if key.strip() == 'MARITACA_API_KEY':
                                    self.api_key = value.strip()
                                    # Remover aspas se houver
                                    if self.api_key.startswith('"') and self.api_key.endswith('"'):
                                        self.api_key = self.api_key[1:-1]
                                    if self.api_key.startswith("'") and self.api_key.endswith("'"):
                                        self.api_key = self.api_key[1:-1]
                                    self.api_key = self.api_key.strip()
                                    os.environ['MARITACA_API_KEY'] = self.api_key
                                    break
        
        # Validação final
        if not self.api_key:
            raise ValueError(
                "API key não fornecida. "
                "Defina MARITACA_API_KEY no arquivo .env, como variável de ambiente ou passe como argumento."
            )
        
        # Limpar espaços e caracteres invisíveis
        self.api_key = self.api_key.strip()
        
        # Validar formato básico
        if len(self.api_key) < 10:
            raise ValueError(f"API key parece inválida (muito curta: {len(self.api_key)} caracteres)")
        
        self.model = "sabia-3.1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
        top_p: float = 0.9,
        stream: bool = False
    ) -> Dict:
        """
        Envia requisição para API de chat completion.
        
        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            temperature: Temperatura para sampling (0.0-2.0)
            max_tokens: Número máximo de tokens a gerar
            top_p: Nucleus sampling parameter
            stream: Se True, retorna stream de respostas
        
        Returns:
            Resposta da API em formato JSON
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição à API: {e}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        top_p: float = 0.9
    ) -> str:
        """
        Gera resposta para um prompt usando a API.
        
        Args:
            prompt: Texto de entrada
            system_prompt: Prompt do sistema (opcional)
            temperature: Temperatura para sampling
            max_tokens: Número máximo de tokens
            top_p: Nucleus sampling parameter
        
        Returns:
            Texto gerado pela API
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )
        
        # Extrair texto da resposta
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Resposta inesperada da API: {response}")
    
    def generate_enem_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> str:
        """
        Gera resposta especializada para questões ENEM.
        
        Args:
            prompt: Questão ou prompt relacionado ao ENEM
            temperature: Temperatura para sampling
            max_tokens: Número máximo de tokens
        
        Returns:
            Resposta gerada
        """
        system_prompt = (
            "Você é um assistente especializado em questões do ENEM (Exame Nacional do Ensino Médio) "
            "e Teoria da Resposta ao Item (TRI). Forneça respostas precisas, didáticas e baseadas "
            "em conhecimento educacional brasileiro."
        )
        
        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )


def test_api_connection(api_key: Optional[str] = None) -> bool:
    """
    Testa conexão com a API.
    
    Args:
        api_key: Chave da API (opcional)
    
    Returns:
        True se conexão bem-sucedida, False caso contrário
    """
    try:
        client = MaritacaAPI(api_key=api_key)
        response = client.generate("Olá, você está funcionando?", max_tokens=50)
        return len(response) > 0
    except Exception as e:
        print(f"Erro ao testar API: {e}")
        return False


if __name__ == "__main__":
    # Teste básico
    print("Testando conexão com API Maritaca...")
    
    try:
        client = MaritacaAPI()
        print("✅ Cliente inicializado com sucesso!")
        
        # Teste simples
        response = client.generate("Explique o que é o ENEM em uma frase.", max_tokens=100)
        print(f"\nResposta da API:\n{response}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

