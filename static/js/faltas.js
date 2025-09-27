async function CarregarFaltas() {
    const req = await fetch('/faltas/api/v1/faltas_mes')
    const dados = await req.json()

    dados.forEach(element => {
        const ul = document.getElementById(`dia-${element.dia}`)
        if (ul) {
            ul.innerHTML += `<li class='faltas'>${element.nome} <button class='excluir' onclick='excluir(${element.id})'> <a href="/faltas/excluir/${element.id}">&#128465; </a></button> </li>`
        }
    })
}

addEventListener('DOMContentLoaded', CarregarFaltas())

