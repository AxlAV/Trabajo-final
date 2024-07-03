from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def validar_ip(ip):
    octetos = ip.split('.')
    if len(octetos) != 4:
        return False
    for octeto in octetos:
        if not octeto.isdigit():
            return False
        if not 0 <= int(octeto) <= 255:
            return False
    return True

def validar_mascara_decimal(mascara):
    return mascara.isdigit() and 0 <= int(mascara) <= 32

def ip_a_binario(ip):
    return ''.join([f'{int(octeto):08b}' for octeto in ip.split('.')])

def binario_a_ip(binario):
    return '.'.join([str(int(binario[i:i+8], 2)) for i in range(0, 32, 8)])

def calcular_subredes(ip, prefijo, num_subredes):
    ip_binario = ip_a_binario(ip)
    prefijo_longitud = prefijo

    bits_necesarios = (num_subredes - 1).bit_length()
    nueva_mascara_longitud = prefijo_longitud + bits_necesarios
    nueva_mascara_binario = '1' * nueva_mascara_longitud + '0' * (32 - nueva_mascara_longitud)
    nueva_mascara = binario_a_ip(nueva_mascara_binario)

    subredes = []
    for i in range(num_subredes):
        subred_binario = ip_binario[:prefijo_longitud] + f'{i:0{bits_necesarios}b}' + '0' * (32 - prefijo_longitud - bits_necesarios)
        subredes.append(binario_a_ip(subred_binario) + f'/{nueva_mascara_longitud}')

    return nueva_mascara, subredes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        mascara = request.form['mascara']
        num_subredes = request.form['num_subredes']
        
        if not validar_ip(ip):
            error = "IP no válida. Por favor, ingrese una IP válida (formato: xxx.xxx.xxx.xxx con valores entre 0 y 255)."
            return render_template('index.html', error=error)
        
        if not validar_mascara_decimal(mascara):
            error = "Máscara no válida. Por favor, ingrese una máscara válida (número entre 0 y 32)."
            return render_template('index.html', error=error)
        
        nueva_mascara, subredes = calcular_subredes(ip, int(mascara), int(num_subredes))
        return render_template('results.html', nueva_mascara=nueva_mascara, subredes=subredes)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
