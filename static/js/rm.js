async function CarregarDados() {

    const tabela = document.getElementById('tabela_rm')
    tabela.innerHTML = '<tr> Carregando dados ... </tr>'

    const req = await fetch('/rm/api/v1/dados')
    const dados = await req.json()

    tabela.innerHTML = ''
    dados.forEach(element => {

        const linha = document.createElement('tr')
        linha.innerHTML = `<td> ${element.rm} </td> <td> ${element.nome} </td> <td> <a href="/rm/excluir/${element.rm}" class='excluir'> Excluir </a> </td>`
        tabela.appendChild(linha)


    });

}

addEventListener("DOMContentLoaded", CarregarDados())

function Buscar(){

    const busca = document.getElementById('busca')

    const linhas = document.querySelectorAll('tbody tr')
 

    linhas.forEach( e => {

        if (e.textContent.includes(busca.value.toUpperCase())){
            e.style.display = ''
        } else {
            e.style.display = 'none'
        }

    })
}