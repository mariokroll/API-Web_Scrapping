import requests
from bs4 import BeautifulSoup
import pandas as pd
from fpdf import FPDF
import sys


class PDF(FPDF):
    def header(self):
        self.image(TEAM, x=7, y=6, w=27)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def extract(teams_dict: dict) -> tuple:
    """
    Extracción de los datos de las APIs y de las páginas web, además del logo del equipo
    """
    global TEAM
    # Lo necesario para lanzar los requests se encuentra en el fichero config.txt
    with open('config.txt', 'r') as f:
        endline = f.readline().strip()
        url = f.readline().strip()
        url_logo = f.readline().strip()
        f.readline()
        headers = f.readline().split(': ')
        headers = {headers[0].strip(): headers[1].strip()}
    # API
    player_season = requests.get(endline, headers=headers)
    # Página web
    prediction = requests.get(url)
    team = input('Introduce el equipo que quieres consultar (Ejemplo: LAL): ')
    # Comprobamos que el equipo introducido es correcto
    if team not in teams_dict.keys():
        print('ERROR: El equipo introducido no es correcto')
        sys.exit()
    # Logo del equipo
    TEAM = BeautifulSoup(requests.get(url_logo).content, 'html.parser').find_all('a', {'title': teams_dict[team]+' Logos'})[0].img['src']
    return player_season, prediction, team


def transform(player_season: requests.models.Response, prediction: requests.models.Response, 
            team_desired: str, teams_dict: dict) -> tuple:
    """
    Transfromamos los datos para que estén en el formato que queremos
    """
    # Convertimos a DataFrame
    df = pd.DataFrame(player_season.json())
    ## APIs
    # Nos quedamos con los jugadores del equipo que queremos consultar y las columnas que nos interesan
    df_team = df.loc[df.Team == team_desired]

    ## Página web
    soup = BeautifulSoup(prediction.content, 'html.parser')
    team = teams_dict[team_desired].split()
    # Obtenemos las cuotas de los equipos
    blocks = soup.find_all('div', {'class': 'cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative'})
    for block in blocks:
        span = block.find('span', {'class': 'font-medium w-full lg:w-1/2 text-center dark:text-white'}).text.split()
        if span[-1] == team[-1]:
            local = False
            break
        elif span[span.index('-')-1] == team[-1]:
            local = True
            break
    data = block.text.split()
    partido = ' '.join(span[:span.index('-')]) + ' - ' + ' '.join(span[span.index('-')+1:])
    equipos = partido.split(' - ')
    cuota_local, cuota_visitante = data[-3], data[-1]
    return df_team, equipos, cuota_local, cuota_visitante, local


def load(team_desired: str, team: pd.DataFrame, equipos: list, cuota_local: str, cuota_visitante: str, local: bool, pdf: FPDF):
    """
    Guardamos datos en pdf e imprimos por pantalla la predicción con sus cuotas
    """
    pdf.output('team.pdf')
    print(f'El próximo partido es:\n\t{equipos[0]} vs {equipos[1]}\nCuotas:\n\t- {equipos[0]}: {cuota_local}\n\t- {equipos[1]}: {cuota_visitante}')
    print('Esta cuota es la más alta encontrada en las casas de apuestas')
    if local:
        if cuota_local < cuota_visitante:
            print(f'Según la cuota, gana {equipos[0]}')
        else:
            print(f'Según la cuota, pierde {equipos[0]}')
    else:
        if cuota_visitante < cuota_local:
            print(f'Según la cuota, gana {equipos[1]}')
        else:
            print(f'Según la cuota, pierde {equipos[1]}')


def create_pdf(team: pd.DataFrame, columns: list):
    """
    Creamos un pdf con las estadísticas de los jugadores del equipo
    """
    pdf = PDF()
    # Queremos que haya dos jugadores por pantalla así que creamos una variable
    # que nos permita saber cuántos jugadores hemos añadido a la página
    count = 0

    # Iteramos por cada jugador para añadir sus estadísticas a la página
    for player in team.Name.values:
        df = team.loc[team.Name == player]
        if count % 2 == 0:
            pdf.add_page()
        pdf.ln(10)
        pdf.set_font('Helvetica', size=17)
        pdf.cell(0, 15, txt=player, align='C')
        pdf.ln()
        pdf.set_font('Helvetica', size=12)
        pdf.cell(0, 10, txt = 'STATS', align='C', border=1)
        pdf.ln()
        for col in columns:
            pdf.cell(100, 8, txt = col, align='L', border=1)
            pdf.cell(0, 8, txt = str(df[col].values[0]), border=1)
            pdf.ln()
        count += 1
    return pdf


if __name__ == '__main__':
    teams_dict = {
        'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets',
        'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves',
        'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 'OKC': 'Oklahoma City Thunder',
        'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHX': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'
    }
    player_season, prediction, team_desired = extract(teams_dict)
    team, equipos, cuota_local, cuota_visitante, local = transform(player_season, prediction, team_desired, teams_dict)
    columnas = [
    'Position', 'Games', 'TwoPointersMade', 'TwoPointersPercentage', 'ThreePointersMade',
    'ThreePointersPercentage', 'Assists', 'Steals', 'BlockedShots', 'Points',
    'PlayerEfficiencyRating', 'TotalReboundsPercentage'
    ]
    pdf = create_pdf(team, columnas)
    load(team_desired, team, equipos, cuota_local, cuota_visitante, local, pdf)