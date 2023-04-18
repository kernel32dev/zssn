<template>
    <div id="relatorios">
        <div id="grid">
            <a href="/api/rel/infeccoes" download="infeccoes.pdf"><button>Resumo das infecções</button></a>
            <a href="/api/rel/recursos" download="recursos.pdf"><button>Recursos por sobreviventes</button></a>
            <a href="/api/rel/recursos-perdidos" download="recursos-perdidos.pdf"><button>Recursos perdidos para infecções</button></a>
            <a href="/api/rel/sob-relatores" download="sob-relatores.pdf"><button>Sobreviventes por número de relatos feitos</button></a>
            <a href="/api/rel/sob-distancia" download="sob-distancia.pdf"><button>Sobreviventes por distância</button></a>
            <a href="/api/rel/sob-pontos" download="sob-pontos.pdf"><button>Sobreviventes por pontos</button></a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Relatorios'
}
</script>

<style scoped>
#relatorios {
    padding: 100px 30px 30px;
}
a, button {
    width: 100%;
}
#grid {
    max-width: 700px;
    display: grid;
    margin: 0 auto;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 20px;
}
</style>
