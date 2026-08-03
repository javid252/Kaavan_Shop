<template>
  <nav class="navigation-bar">

    <div class="container nav-inner">


      <!-- All Categories -->
      <button class="all-category-btn">
        <span>☰</span>
        همه دسته‌بندی‌ها
      </button>



      <!-- Menu -->
      <div class="nav-links">

        <router-link 
          to="/"
          exact
        >
          خانه
        </router-link>


        <router-link 
          to="/products"
        >
          محصولات
        </router-link>


        <router-link 
          v-if="multivendorEnabled"
          to="/stores"
        >
          فروشگاه‌ها
        </router-link>


        <router-link 
          to="/products?featured=1"
        >
          پیشنهاد ویژه
        </router-link>


        <router-link 
          to="/products?sort=newest"
        >
          جدیدترین‌ها
        </router-link>


        <router-link 
          to="/products?sort=popular"
        >
          پرفروش‌ترین‌ها
        </router-link>


        <router-link 
          to="/contact"
        >
          تماس با ما
        </router-link>


      </div>


    </div>

  </nav>
</template>



<script>

import {mapGetters} from "vuex";


export default {

name:"NavigationBar",


computed:{

...mapGetters(
"platform",
[
"multivendorEnabled"
]
)

}


};

</script>



<style scoped>


.navigation-bar{

background:var(--color-surface);

border-bottom:1px solid var(--color-border);

}



.nav-inner{

height:52px;

display:flex;

align-items:center;

gap:20px;

}



/* CATEGORY BUTTON */


.all-category-btn{

height:38px;

padding:0 20px;

border:none;

border-radius:var(--radius-sm);

background:var(--color-primary);

color:white;

font-family:inherit;

font-weight:700;

display:flex;

align-items:center;

gap:8px;

white-space:nowrap;

}





/* LINKS */


.nav-links{

display:flex;

align-items:center;

gap:28px;

height:100%;

}



.nav-links a{

font-size:.9rem;

font-weight:600;

color:var(--color-text-muted);

position:relative;

height:100%;

display:flex;

align-items:center;

}





.nav-links a:hover{

color:var(--color-primary);

}



.nav-links a.router-link-active{

color:var(--color-primary);

}



.nav-links a.router-link-active::after{

content:"";

position:absolute;

bottom:0;

right:0;

left:0;

height:3px;

background:var(--color-accent);

}




@media(max-width:900px){


.nav-inner{

overflow-x:auto;

}



.nav-links{

gap:20px;

}



.all-category-btn{

font-size:.85rem;

}



}


</style>