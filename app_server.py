import os
import subprocess

import pygetwindow as gw
from elevate import elevate
from flask import Flask, render_template 

dict_machine = {}
machine_name = 'Engine_06' #Precisa colocar o da máquina

#Verificar e colocar os paths dos executáveis desejados
list_programs_path = ['C:\\Program Files\\Vizrt\\Viz3\\viz.exe -u1 -y -n', 'C:\\Program Files\\Vizrt\\Viz3\\viz.exe -u2 -y -n', 'C:\\iHOP4\\HOP_Console.exe']

app = Flask(__name__)

@app.route('/<command>/<program>', methods = ["GET"])
def call_command_app(command,program):
	try:
		program_ = 'program_' + program
		if command == 'open':
			try:
				check = check_app_status(dict_machine[program_]['name_window'])
				if program == 'iHop' and check == 'Fechado':
					os.system('start ' + dict_machine[program_ ]['path'])
					dict_machine[program_ ]['status'] = 'Aberto'
					return '<h1>Abrindo o programa ' + dict_machine[program_ ]['path'] +'</h1>'
			
				elif check == 'Fechado':
					subprocess.Popen(dict_machine[program_]['path'])
					dict_machine[program_ ]['status'] = 'Aberto'
					return '<h1>Abrindo o programa ' + dict_machine[program_]['path'] +'</h1>'  

				else:
					return '<h1>Aplicação já está aberta</h1>'

			except Exception as e:
				return '<h2>Problemas com o nome da aplicação: '+ str(e) + '</h2>'
		
		elif command == 'close':
			try:
				check = check_app_status(dict_machine[program_ ]['name_window'])
				if check == 'Aberto':
					subprocess.Popen("taskkill /f /t /im " + dict_machine[program_ ]['name_kill'])
					return '<h1>Fechando aplicação ' + dict_machine[program_ ]['name'] + '</h1>'
				else:
					return '<h1>Aplicação já está fechada</h1>'
			except Exception as e:
				return '<h2>Problemas com o nome da aplicação: '+ str(e) + '</h2>'
		
		else:
			return '<div><h2>Problemas de comando as opções são [open] ou [close]</h2></div>'
	
	except Exception as e:
		return '<div><h2>Problemas com o comando passado: '+ str(e) + '</h2></div>'
		
@app.route('/check')
def show_status():
	for program in dict_machine:
		new_status = check_app_status(dict_machine[program]['name_window'])
		dict_machine[program]['status'] = new_status

	return  render_template('check.html', dict_machine = dict_machine, title=machine_name)

def check_app_status(App):
	list_of_windows = gw.getAllTitles()
	
	if App in list_of_windows:
		return 'Aberto'
	else:
		return 'Fechado'
	

#Atualizar a função create_dictionary para bater com a list_programs_paths
def create_dictionary():
	dict_machine.clear()
	for program_number in range(len(list_programs_path)):
		
		temp = os.path.split(list_programs_path[program_number]) ##separa em duas string na ultima '\' do path
		status = 'Not Checked'
		
		if temp[1] == 'viz.exe -u1 -y -n':
			name_app = 'Viz_1'
			name_kill = os.path.splitext(temp[1])
			name_window = 'X64 Viz Engine [1]'

		elif temp[1] == 'viz.exe -u2 -y -n':
			name_app = 'Viz_2'
			name_kill = os.path.splitext(temp[1])
			name_window = 'X64 Viz Engine [2]'

		elif temp[1] == 'HOP_Console.exe':
			name_app = 'iHop'
			name_kill = os.path.splitext(temp[1])
			name_window = 'iHOP Proxy'

		else:
			name_app=name_kill=name_window=status = 'Nenhuma correspondencia encontrada'
	
		dict_machine['program_' + name_app] = {'name': name_app,'path':list_programs_path[program_number], 'status': status, 'name_kill': name_kill[0] + '.exe', 'name_window': name_window}


if __name__ == '__main__':
	elevate(show_console=True)
	create_dictionary()
	app.run(host='0.0.0.0', debug=False) ###host='0.0.0.0', deixa o ip público, roda a aplicação na porta 5000 por padrão
	#Para mudar a porta usar:    app.run(port = NUMERODAPORTA)
	