<template>
    <div id="relatorios">
        <div id="grid">
            <button>Resumo das infecções</button>
            <button>Recursos por sobreviventes</button>
            <button>Recursos perdidos para infecções</button>
            <button>Sobreviventes por número de relatos feitos</button>
            <button>Sobreviventes por distância</button>
            <button>Sobreviventes por pontos</button>
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
#grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 20px;
}
</style>
