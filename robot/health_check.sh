#!/bin/bash

echo "========== VERIFICAÇÃO DE SAÚDE DO CONTAINER UR5 =========="

# Verificar processos em execução
echo "Processos em execução:"
ps -aux | grep -E "python|Xvfb|x11vnc|novnc|websockify"

# Verificar serviços do supervisor
echo -e "\nStatus dos serviços supervisor:"
supervisorctl status

# Verificar se o X server está funcionando
echo -e "\nVerificação do servidor X:"
if xdpyinfo -display :1 > /dev/null 2>&1; then
  echo "X Server :1 está funcionando corretamente"
else
  echo "ERRO: X Server :1 não está funcionando"
fi

# Verificar se o VNC está funcionando
echo -e "\nVerificação do servidor VNC:"
if netstat -tuln | grep -q ":5900"; then
  echo "Servidor VNC está funcionando corretamente na porta 5900"
else
  echo "ERRO: Servidor VNC não está funcionando na porta 5900"
fi

# Verificar se o websockify (noVNC) está funcionando
echo -e "\nVerificação do websockify (noVNC):"
if netstat -tuln | grep -q ":80"; then
  echo "Websockify está funcionando corretamente na porta 80"
else
  echo "ERRO: Websockify não está funcionando na porta 80"
fi

# Verificar conexão com MQTT
echo -e "\nVerificação do MQTT:"
if ping -c 1 mqtt > /dev/null 2>&1; then
  echo "Servidor MQTT está acessível"
else
  echo "AVISO: Servidor MQTT não está acessível"
fi

# Verificar logs de erros
echo -e "\nÚltimas linhas de log do simulador:"
tail -n 10 /var/log/supervisor/simulator*.log

echo -e "\nÚltimas linhas de log de erro do simulador:"
tail -n 10 /var/log/supervisor/simulator-error.log

echo -e "\nÚltimas linhas de log do Xvfb:"
tail -n 10 /var/log/supervisor/xvfb*.log

echo "========== FIM DA VERIFICAÇÃO ==========" 