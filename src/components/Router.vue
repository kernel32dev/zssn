<template>
    <div id="router" :class="{open_drawer: open_drawer}">
        <div id="drawer">
            <div id="drawer-space">
                <div id="drawer-header" @click="open_drawer = false">
                    <div class="drawer-icon overlapped bars">&#xf0c9;</div>
                    <div class="drawer-icon overlapped chevron">&#xf078;</div>
                </div>
                <router-link :to="{ name: 'home' }">
                    <div class="drawer-item">
                        <div class="drawer-icon">&#xf007;</div>
                        Meu Perfil
                    </div>
                </router-link>
                <router-link :to="{ name: 'comprar' }">
                    <div class="drawer-item">
                        <div class="drawer-icon">&#xf4c0;</div>
                        Comprar
                    </div>
                </router-link>
                <router-link :to="{ name: 'vender' }">
                    <div class="drawer-item">
                        <div class="drawer-icon">&#xf4c1;</div>
                        Vender
                    </div>
                </router-link>
                <router-link :to="{ name: 'relatos' }">
                    <div class="drawer-item">
                        <div class="drawer-icon">! &#xf0a4;</div>
                        Relatos
                    </div>
                </router-link>
                <router-link :to="{ name: 'relatorios' }">
                    <div class="drawer-item">
                        <div class="drawer-icon">&#xf15c;</div>
                        Relatórios
                    </div>
                </router-link>
            </div>
        </div>
        <div id="router-root">
            <div id="router-header">
                <div class="drawer-icon drawer-open-button" @click="open_drawer = true">&#xf0c9;</div>
                <div id="router-title">{{ $route.meta.alias }}</div>
            </div>
            <router-view/>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Router',
    data() {
        return {
            open_drawer: false
        }
    },
    mounted() {
        let router_root = this.$el.lastElementChild;
        let self = this;
        function filter_event(ev) {
            if (!self.open_drawer) {
                return;
            }
            ev.stopPropagation();
            ev.preventDefault();
            if (ev.type === 'mousedown' || ev.type === 'touchstart') {
                self.open_drawer = false;
            }
        }
        router_root.addEventListener('mousedown', filter_event);
        router_root.addEventListener('touchstart', filter_event);
        router_root.addEventListener('scroll', filter_event);
        let items = document.getElementsByClassName('drawer-item');
        for (let i = 0; i < items.length; i++) {
            items[i].parentElement.addEventListener('click',
                function () {
                    self.open_drawer = false
                }
            );
        }
    }
}
</script>

<style>
#router {
    color: #2c3e50;
    background-color: black;
    padding-top: var(--title-height);
}
#router, #router-root {
    min-height: calc(100vh - var(--title-height));
}
#drawer {
    position: fixed;
    left: 0px;
    bottom: 0px;
    width: var(--drawer-closed);
    min-height: 100vh;
    background-color: var(--theme-color);
    transition: width var(--anim-time) ease, box-shadow var(--anim-time) cubic-bezier(1,0,1,0);
    overflow: hidden;
    box-shadow: black -10px 0px 10px 10px;
    z-index: 3;
}
#drawer:hover, #router.open_drawer #drawer {
    width: var(--drawer-open);
}
#drawer a { text-decoration: none; }
body.mobile #drawer {
    width: 0px;
    box-shadow: black -20px 0px 10px 10px;
}
body.mobile #drawer:hover, body.mobile #router.open_drawer #drawer {
    box-shadow: black -10px 0px 10px 10px !important;
}
#router-root {
    opacity: 1;
    background-color: white;
    transition: opacity var(--anim-time) ease;
    z-index: 1;
}
body.desktop #router-root {
    margin-left: var(--drawer-closed);
}
#router.open_drawer #router-root {
    opacity: 0.3;
}
#drawer-space {
    width: var(--drawer-open);
}
#router-header {
    position: fixed;
    top: 0px;
    height: var(--title-height);
    background-color: var(--theme-color);
    box-shadow: black 0px -10px 10px 10px;
    display: flex;
    flex-direction: row;
    align-items: end;
    z-index: 2;
}
body.mobile #router-header {
    left: 0px;
    width: 100%;
}
body.desktop #router-header {
    left: var(--drawer-closed);
    width: calc(100% - var(--drawer-closed));
}
#router-title {
    margin-bottom: 10px;
    margin-left: 15px;
    font-size: calc(var(--title-height) * 0.5);
}
#drawer-header {
    height: var(--icon-size);
}
.drawer-item {
    display: flex;
    align-items: center;
    user-select: none;
    cursor: pointer;
    flex-direction: row;
    color: black;
    transition: background-color var(--anim-time) ease;
    font-size: medium;
}
.drawer-item:hover {
    background-color: rgba(0,0,0,0.3);
}
.drawer-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    user-select: none;
    font-family: 'Font Awesome 6 Free';
    width: var(--icon-size);
    height: var(--icon-size);
}
.drawer-icon.overlapped {
    position: absolute;
    transition: opacity var(--anim-time) ease;
}
#drawer:hover .drawer-icon.overlapped.chevron,
#router.open_drawer .drawer-icon.overlapped.chevron,
.drawer-icon.overlapped.bars
{
    opacity: 1;
}
#drawer:hover .drawer-icon.overlapped.bars,
#router.open_drawer .drawer-icon.overlapped.bars,
.drawer-icon.overlapped.chevron
{
    opacity: 0;
}
body.desktop .drawer-open-button {
    display: none;
}
</style>
