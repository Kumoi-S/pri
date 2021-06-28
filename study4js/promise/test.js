let p1 = new Promise((resolve, reject) => {
  resolve("成功");
});
console.log(p1);

new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("fulfilled");
  }, 2000);
}).then(
  (msg) => {
    console.log(msg);
  },
  (error) => {
    console.log(error);
  }
);
