<template>
  <section class="category-section">
    <div class="container">
      <div class="section-header">
        <span class="eyebrow">
          دسته‌بندی‌ها
        </span>       
      </div>
      <div class="category-grid">
        <router-link
          v-for="cat in categories"
          :key="cat.id"
          :to="`/products?category=${cat.slug}`"
          class="category-item"
        >
          <div class="category-image">
            <img
              v-if="cat.image"
              :src="cat.image"
              :alt="cat.name"
            />
            <span v-else>
              {{ cat.icon || "🛍️" }}
            </span>
          </div>
          <div class="category-name">
            {{cat.name}}
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script>
    export default{
        name:"CategoryGrid",
        props:{
            categories:{
                type:Array,
                default:()=>[]
            }
        }
    };
</script>

<style scoped>

.category-section{
    padding:15px 0 35px;
}



.section-header{
    text-align:center;
    margin-bottom:0px;
}



.section-header h2{

font-size:1.6rem;

margin-top:8px;

}



.category-grid{


display:grid;

grid-template-columns:
repeat(auto-fit,minmax(120px,1fr));

gap:30px;

}



.category-item{


display:flex;

flex-direction:column;

align-items:center;

gap:12px;

transition:.2s;


}



.category-item:hover{


transform:translateY(-5px);


}



.category-image{


width:110px;

height:110px;

border-radius:50%;

overflow:hidden;

background:var(--color-sand);

border:4px solid var(--color-surface);

box-shadow:var(--shadow-md);

display:flex;

align-items:center;

justify-content:center;

font-size:2.5rem;


}



.category-image img{


width:100%;

height:100%;

object-fit:cover;


}



.category-name{


font-weight:700;

font-size:.95rem;

color:var(--color-text);


}



@media(max-width:600px){


.category-grid{

grid-template-columns:

repeat(3,1fr);

gap:20px;

}



.category-image{

width:85px;

height:85px;

}


}



</style>