function Queue() {
  let queue = [];
  this.enqueue = (element) => { queue.push(element); }
  this.dequeue = () => { return queue.shift(); }
  this.front = () => { return queue[0]; }
  this.isEmpty = () => { return queue.length === 0; }
  this.clear = () => { queue = []; }
  this.size = () => { return queue.length; }
  this.print = () => { return queue.toString(); }
}