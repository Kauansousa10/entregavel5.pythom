import csv
import re
from datetime import datetime


class FormatoInvalidoError(Exception):
    pass


def validar_email(email):
    return bool(re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email))


def validar_cpf(cpf):
    return bool(re.match(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$", cpf))


def validar_telefone(telefone):
    return bool(re.match(r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$", telefone))


def validar_data(data):
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", data):
        return False

    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_registro(registro):

    for campo in ["email", "cpf", "telefone", "data"]:
        if campo not in registro:
            raise KeyError(campo)

    if not validar_email(registro["email"]):
        raise FormatoInvalidoError("E-mail inválido")

    if not validar_cpf(registro["cpf"]):
        raise FormatoInvalidoError("CPF inválido")

    if not validar_telefone(registro["telefone"]):
        raise FormatoInvalidoError("Telefone inválido")

    if not validar_data(registro["data"]):
        raise FormatoInvalidoError("Data inválida")

    return True


def analisar_arquivo(nome_arquivo):

    validos = []
    invalidos = []
    total = 0

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:

            leitor = csv.DictReader(arquivo)

            try:
                campos = leitor.fieldnames or []

                for campo in ["email", "cpf", "telefone", "data"]:
                    if campo not in campos:
                        raise KeyError(campo)

                for numero, registro in enumerate(leitor, start=2):

                    total += 1

                    try:
                        validar_registro(registro)
                        validos.append((numero, registro))

                    except (FormatoInvalidoError, KeyError) as erro:
                        invalidos.append(
                            (numero, registro, str(erro))
                        )

            except KeyError as erro:
                print(f"Coluna ausente: {erro}")

            else:
                print("Arquivo lido com sucesso!")

    except FileNotFoundError:
        print("Erro: arquivo não encontrado.")

    except ValueError as erro:
        print(f"Erro de conversão: {erro}")

    finally:
        print("Leitura do arquivo finalizada.")

    return total, validos, invalidos


def gerar_relatorio(total, validos, invalidos):

    percentual = len(validos) / total * 100 if total else 0

    try:
        with open("relatorio.txt", "w", encoding="utf-8") as arquivo:

            arquivo.write("===== RELATÓRIO =====\n")
            arquivo.write(f"Total: {total}\n")
            arquivo.write(f"Válidos: {len(validos)}\n")
            arquivo.write(f"Inválidos: {len(invalidos)}\n")
            arquivo.write(f"Percentual válido: {percentual:.2f}%\n\n")

            arquivo.write("DADOS VÁLIDOS:\n")

            for numero, registro in validos:
                arquivo.write(
                    f"Linha {numero}: "
                    f"{registro['email']} | "
                    f"{registro['cpf']} | "
                    f"{registro['telefone']} | "
                    f"{registro['data']}\n"
                )

            arquivo.write("\nDADOS INVÁLIDOS:\n")

            for numero, registro, erro in invalidos:
                arquivo.write(
                    f"Linha {numero}: {erro}\n"
                )

    except OSError as erro:
        print(f"Erro ao criar relatório: {erro}")

    else:
        print("Relatório criado com sucesso!")

    finally:
        print("Finalização do relatório.")


def main():

    total, validos, invalidos = analisar_arquivo("dados.csv")

    if total > 0:
        gerar_relatorio(total, validos, invalidos)


if _name_ == "_main_":
    main()