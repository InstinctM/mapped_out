function pageTransition() {

    var tl = gsap.timeline();

    tl.to('ul.cf li', { duration: .5, scaleY: 1, transformOrigin: "bottom left", stagger: .2})
    tl.to('ul.cf li', { duration: .5, scaleY: 0, transformOrigin: "bottom left", stagger: .1, delay: .1})
}

function contentAnimation() {}

    var tl = gsap.timeline();
    
    tl.from('.showcase', { duration: 1.5, translateY: 50, opacity: 0})
    tl.to('overview', { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0% 100%)"})


function delay(n) {
    n = n || 2000
    return new Promise(done => {
      setTimeout(() => {
          done();
    }, n);
  });
}

barba.init({
    sync: true,

    transitions: [{

        async leave(data) {

            const done = this.async();

            pageTransition();
            await delay(1500);
            done();
        },

        async enter(data) {
            contentAnimation();
        },
        async once(data) {
            contentAnimation();
        }
    }]
})



const cookieBox = document.querySelector(".wrapper"),
            acceptBtn = cookieBox.querySelector("button");
            acceptBtn.onclick = ()=>{
              //setting cookie for 1 month, after one month it'll be expired automatically
              document.cookie = "CookieBy=CodingNepal; max-age="+60*60*24*30;
              if(document.cookie){ //if cookie is set
                cookieBox.classList.add("hide"); //hide cookie box
              }else{ //if cookie not set then alert an error
                alert("Cookie can't be set! Please unblock this site from the cookie setting of your browser.");
              }
            }
            let checkCookie = document.cookie.indexOf("CookieBy=CodingNepal"); //checking our cookie
            //if cookie is set then hide the cookie box else show it
            checkCookie != -1 ? cookieBox.classList.add("hide") : cookieBox.classList.remove("hide");















// // Page Transition
// function transitionAnimation(){
//     gsap.to("loader-overlay.one", {
//         duration: 1,
//         scaleX: 1,
//         transformOrigin: "left", 
//         ease: "power1.inOut"
//     });
//     gsap.to("loader-overlay.one", {
//         duration: 1,
//         scaleX: 0,
//         transformOrigin: "right", 
//         ease: "power1.inOut",
//         delay: 2
//     });
//     gsap.to("loader-overlay.two", {
//         duration: 1.4,
//         scaleX: 1,
//         transformOrigin: "left", 
//         ease: "power1.inOut"
//     });
//     gsap.to("loader-overlay.two", {
//         duration: 1.4,
//         scaleX: 0,
//         transformOrigin: "right", 
//         ease: "power1.inOut",
//         delay: 1.6
//     });
// }


// // Page Delay - Promise Function

// function delay(n) {

//     n = n || 4000; //default time set
//     return new Promise((done) => {
//         setTimeout(() => {
//             done();
//         }, n) ;
//     }) ;
// }



// $(function(){

// // Barba Setup
// barba.init({
//     sync: true,

//     transitions: [{
      
//       async leave(data) {
//         // create your stunning leave animation here
//         const done = this.async();
//         setTimeout(function(){
//             transitionAnimation();
//         }, 2000);
//         await delay(3000);
//         done();
//       },
//       async enter(data) {
//         // create your amazing enter animation here
//       }
//     }]
//   });

// });