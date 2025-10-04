async function CarregarDados() {

    const tabela = document.getElementById('turmas')

    const req = await fetch('/lp/api/v1/dados')
    const dados = await req.json()

    dados.forEach(element => {

        const linha = document.createElement('tr')
        linha.innerHTML = `<td> ${element.id} </td> <td> ${element.desc} </td> <td><a href="/lp/delete/${element.id}" class='excluir'>Excluir</a></td>`
        tabela.appendChild(linha)
    })

}

addEventListener('DOMContentLoaded', CarregarDados())
