#sudo pip install pysnmp pysnmp-mibs
import urllib2,time
from pysnmp.entity.rfc3413.oneliner import cmdgen

__author__ = 'Guardiao Cloud'

apiKey = "xxxxxxxx-yyyy-zzzz-wwww-kkkkkkkkkkkk" #@todo Alterar Numero da API Key
serialKey = "GUC0001" #@todo Alterar numero de serie do dispositivo de Coleta
checkedTime = 60  #Tempo em segundos de coleta e envio das informacoes

snmpPort = 161 #@todo Alterar porta do SNMP
snmpIP = '127.0.0.1' #@todo Alterar IP da maquina com SNMP
snmpCommunity = 'public' #@todo Alterar comunidade padrao SNMP

#Mapa contendo o oid=nomeEnvio
mapaGuardiao = {}
mapaGuardiao['.1.3.6.1.4.1.2021.10.1.3.1'] = 'load1min' # Chave 1
mapaGuardiao['.1.3.6.1.4.1.2021.10.1.3.2'] = 'load5min' # Chave 2
mapaGuardiao['.1.3.6.1.4.1.2021.10.1.3.3'] = 'load15min' # Chave 3

if __name__ == '__main__':
    while True:
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(snmpCommunity, mpModel=0),
            cmdgen.UdpTransportTarget((snmpIP, snmpPort)),
            cmdgen.MibVariable('.1.3.6.1.4.1.2021.10.1.3.1'), # Mesmo valor da Chave 1
            cmdgen.MibVariable('.1.3.6.1.4.1.2021.10.1.3.2'), # Mesmo valor da Chave 2
            cmdgen.MibVariable('.1.3.6.1.4.1.2021.10.1.3.3'), # Mesmo valor da Chave 3

        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                valorEnvio = ""
                for name, val in varBinds:
                    chave = mapaGuardiao["."+name.prettyPrint()] #Fazendo um parse baseado na chave para geração da URL
                    valor = val.prettyPrint()
                    valorEnvio += "{0}={1}&".format(chave,int(valor))
                url = "http://guardiao.cl/collect/{0}/?{1}apiKey={2}".format(serialKey,valorEnvio,apiKey)
                print urllib2.urlopen(url).read()
        time.sleep(checkedTime)