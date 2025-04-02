document.addEventListener("DOMContentLoaded", function() {
 
    document.getElementById("criarMesa").addEventListener("click", function() {
        let numeroMesa = prompt("Digite o número da nova mesa:");
        if (numeroMesa) {
            fetch("/criar_mesa", {
                method: "POST",
                body: JSON.stringify({ numero: numeroMesa }),
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.mensagem);
                location.reload();
            });
        }
    });

    document.querySelectorAll(".mesa").forEach(mesa => {
        mesa.addEventListener("contextmenu", function(event) {
            event.preventDefault();
            let mesaId = this.getAttribute("data-id");
            let mesaNumero = this.innerText;
            fetch(`/mesa/${mesaId}/nota`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert(data.erro);
                    return;
                }
              
                document.getElementById("notaMesaNumero").innerText = mesaNumero;
                document.getElementById("notaTotal").innerText = data.total.toFixed(2);
                let conteudo = document.getElementById("notaConteudo");
                conteudo.innerHTML = "";
                let tabela = document.createElement("table");
                tabela.className = "table table-bordered";
                tabela.innerHTML = `
                  <thead>
                    <tr>
                      <th>Produto</th>
                      <th>Preço Unitário</th>
                      <th>Quantidade</th>
                      <th>Subtotal</th>
                    </tr>
                  </thead>
                  <tbody></tbody>
                `;
                let tbody = tabela.querySelector("tbody");
                data.itens.forEach(item => {
                    let tr = document.createElement("tr");
                    tr.innerHTML = `
                      <td>${item.nome}</td>
                      <td>R$ ${item.preco.toFixed(2)}</td>
                      <td>${item.quantidade}</td>
                      <td>R$ ${item.subtotal.toFixed(2)}</td>
                    `;
                    tbody.appendChild(tr);
                });
                conteudo.appendChild(tabela);
                document.getElementById("confirmarFecharMesa").setAttribute("data-mesa", mesaId);
                $("#modalNota").modal("show");
            });
        });
    });

    document.getElementById("confirmarFecharMesa").addEventListener("click", function() {
        let mesaId = this.getAttribute("data-mesa");
        fetch(`/mesa/${mesaId}/fechar`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            $("#modalNota").modal("hide");
            location.reload();
        });
    });

    document.querySelectorAll(".mesa").forEach(mesa => {
        mesa.addEventListener("click", function(event) {
            if (event.button === 2) return;
            let mesaId = this.getAttribute("data-id");
            let mesaNumero = this.innerText;
            document.getElementById("mesaNumero").innerText = mesaNumero;
            document.getElementById("modalMesa").dataset.mesa = mesaId;
            
            fetch(`/mesa/${mesaId}/produtos`)
            .then(response => response.json())
            .then(data => {
                let listaProdutos = document.getElementById("listaProdutos");
                listaProdutos.innerHTML = "";
                data.forEach(produto => {
                    let li = document.createElement("li");
                    li.innerHTML = `
                      <div class="d-flex justify-content-between align-items-center">
                        <span>${produto.nome} - ${produto.quantidade}x</span>
                        <div>
                          <!-- Campo para digitar a nova quantidade -->
                          <input 
                            type="number" 
                            class="form-control input-sm nova-quantidade" 
                            data-mesa="${mesaId}" 
                            data-produto="${produto.id}" 
                            value="${produto.quantidade}"
                          >
                          <!-- Botão para confirmar a atualização da quantidade -->
                          <button 
                            class="btn btn-primary btn-sm atualizar-quantidade" 
                            data-mesa="${mesaId}" 
                            data-produto="${produto.id}"
                          >
                            Atualizar
                          </button>
                          <!-- Botão de remover produto -->
                          <button 
                            class="btn btn-danger btn-sm remover-produto" 
                            data-mesa="${mesaId}" 
                            data-produto="${produto.id}"
                          >
                            ❌
                          </button>
                        </div>
                      </div>
                    `;
                    listaProdutos.appendChild(li);
                });
            });
            fetch("/buscar_produtos")
            .then(response => response.json())
            .then(data => {
                let select = document.getElementById("selectProduto");
                select.innerHTML = "";
                data.forEach(produto => {
                    let option = document.createElement("option");
                    option.value = produto.id;
                    option.textContent = produto.nome;
                    select.appendChild(option);
                });
            });

            $("#modalMesa").modal("show");
        });
    });

    document.getElementById("listaProdutos").addEventListener("click", function(event) {

        if (event.target.classList.contains("atualizar-quantidade")) {
            let button = event.target;
            let mesaId = button.getAttribute("data-mesa");
            let produtoId = button.getAttribute("data-produto");
            let input = button.parentElement.querySelector(".nova-quantidade");
            let quantidade = parseInt(input.value);
            if (isNaN(quantidade) || quantidade < 0) {
                alert("Por favor, insira uma quantidade válida.");
                return;
            }
            fetch(`/mesa/${mesaId}/alterar_quantidade/${produtoId}`, {
                method: "PUT",
                body: JSON.stringify({ quantidade: quantidade }),
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.mensagem);
                location.reload();
            });
        }

        else if (event.target.classList.contains("remover-produto")) {
            let button = event.target;
            let mesaId = button.getAttribute("data-mesa");
            let produtoId = button.getAttribute("data-produto");
            if (confirm("Deseja remover este produto da mesa?")) {
                fetch(`/mesa/${mesaId}/remover_produto/${produtoId}`, { method: "DELETE" })
                .then(response => response.json())
                .then(data => {
                    alert(data.mensagem);
                    $("#modalMesa").modal("hide");
                    location.reload();
                });
            }
        }
    });


    document.getElementById("buscaProduto").addEventListener("input", function() {
        let termo = this.value.toLowerCase();
        fetch("/buscar_produtos")
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById("selectProduto");
            select.innerHTML = "";
            data.forEach(produto => {
                if (produto.nome.toLowerCase().includes(termo)) {
                    let option = document.createElement("option");
                    option.value = produto.id;
                    option.textContent = produto.nome;
                    select.appendChild(option);
                }
            });
        });
    });


    document.getElementById("adicionarProduto").addEventListener("click", function() {

        let mesaId = document.getElementById("modalMesa").dataset.mesa;
        let produtoId = document.getElementById("selectProduto").value;
        let quantidade = parseInt(document.getElementById("quantidade").value);
        if (!quantidade || quantidade <= 0) {
            alert("Por favor, insira uma quantidade válida.");
            return;
        }
        fetch(`/mesa/${mesaId}/adicionar_produto`, {
            method: "POST",
            body: JSON.stringify({ produto_id: produtoId, quantidade: quantidade }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            $("#modalMesa").modal("hide");
            location.reload();
        });
    });
});
