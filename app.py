from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)   

clientes = []
veiculos = []

@app.route('/')  
def index():
    return redirect(url_for('veiculos_page'))   #vai jogar o usuario para pagina de veiculos 

@app.route('/clientes', methods=['GET', 'POST']) #carrega pagina e envia os formularios dos dados dos clientes
def clientes_page():
    if request.method == 'POST': # função para verifica o formulario preenchido para cadastrar o cliente
        novo_cliente = {
            'id': len(clientes) + 1, #gera um id unico
            'nome': request.form['nome'],
            'cpf': request.form['cpf'],
            'telefone': request.form['telefone'],
            'obs': request.form['obs']
        }
        clientes.append(novo_cliente) #adicona o cliente cadastrado na lista
        return redirect(url_for('clientes_page')) #volta pra pagina
    
    return render_template('clientes.html', clientes=clientes) 
#carrega a pagina de clientes para o template hrml 

@app.route('/veiculos', methods=['GET', 'POST'])
def veiculos_page():
    if request.method == 'POST' and 'modelo' in request.form:
        novo_veiculo = {
            'id': len(veiculos) + 1,
            'modelo': request.form['modelo'], 
            'placa': request.form['placa'],
            'status': 'Disponível', #definir que o status fique disponivel 
            'cliente_id': None #não foi alugado ainda
        }
        veiculos.append(novo_veiculo)
        return redirect(url_for('veiculos_page'))

    busca = request.args.get('busca', '').lower() #deixa sempre minusculo pra padronizar busca
    veiculos_filtrados = veiculos
    if busca:
        veiculos_filtrados = [v for v in veiculos if busca in v['modelo'].lower() or busca in v['placa'].lower()]

    return render_template('veiculos.html', veiculos=veiculos_filtrados, clientes=clientes, busca=busca)
#se o veiculo estiver preenchido ele vai ser adcionado e vai retornar ao template veiculos os dados inputados

@app.route('/alugar/<int:veiculo_id>', methods=['POST'])
def alugar_veiculo(veiculo_id):
    cliente_id = request.form.get('cliente_id')
    for v in veiculos:  #compara o id do veiculo com o id do veiculo que foi clicado para alugar ou devolver
        if v['id'] == veiculo_id:  #valida se o veiculo e o mesmo que foi locado 
            if cliente_id:  
                v['status'] = 'Alugado' #se for selecionado cliente muda para alugado 
                v['cliente_id'] = int(cliente_id)
            else:  # se não for selecionado ele teria sido devolvido então fica como disponivel
                v['status'] = 'Disponível'
                v['cliente_id'] = None  #remove o cliente associado ao veiculo
            break #quebra pra não bugar tudo!!!!!!!!!!!!!!!!!!
    return redirect(url_for('veiculos_page')) #retorna a pagina apos atualizar o status do veiculo

if __name__ == '__main__': #executa codigo somente se for o arquivo principal
    app.run(debug=True) #inicia sempre em debug para mostrar erros do flask 