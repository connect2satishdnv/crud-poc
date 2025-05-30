# --- File: cli/main.py ---
import click
import os
import requests
import json

API_URL = "http://api:8000"
TOKEN_FILE = os.path.expanduser("~/.cli_token")

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()['access_token']
        save_token(token)
        click.echo("Login successful.")
    else:
        click.echo("Login failed.")

@cli.command()
@click.argument('title')
def create_task(title):
    token = load_token()
    headers = {"Authorization": f"Bearer {token}"}
    task = {"id": len(get_tasks()), "title": title}
    response = requests.post(f"{API_URL}/tasks", json=task, headers=headers)
    click.echo(response.json())

@cli.command()
def get_tasks():
    token = load_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/tasks", headers=headers)
    click.echo(json.dumps(response.json(), indent=2))
    return response.json()

@cli.command()
@click.argument('task_id', type=int)
def delete_task(task_id):
    token = load_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/tasks/{task_id}", headers=headers)
    click.echo(response.json())

if __name__ == '__main__':
    cli()
