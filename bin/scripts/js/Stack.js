function Stack () {
  let stack = [];

  this.push = (element) => { stack.push(element); }
  this.pop = () => { return stack.pop(stack.length-1); }
  this.peek = () => { return stack[stack.length-1]; };
  this.isEmpty = () => { return stack.length === 0; };
  this.clear = () => { stack = []; }
  this.size = () => { return stack.length; }
  this.print = () => { return stack.toString(); }
}

/** ES6 CLASS WITH WEAKMAP */

// let Stack = (function () {
//   const stack = new WeakMap();
//   class Stack {
//     constructor() { stack.set(this, []); }

//     push(element) { stack.get(this).push(element); }
//     pop() { return stack.get(this).pop(stack.get(this).length-1); }
//     peek() { return stack.get(this)[stack.get(this).length - 1]; };
//     isEmpty() { return stack.get(this).length === 0; };
//     clear() { stack.get(this) = []; }
//     size() { return stack.get(this).length; }
//     print() { return stack.get(this).toString(); }
//   }
//   return Stack;
// }) ();