// Advantages over arrays
// 1) Dynamic size
// 2) Ease of insertion/deletion

// Drawbacks:
// 1) Random access is not allowed. We have to access elements sequentially starting from the first node. So we cannot do binary search with linked lists efficiently with its default implementation. Read about it here.
// 2) Extra memory space for a pointer is required with each element of the list.
// 3) Not cache friendly. Since array elements are contiguous locations, there is locality of reference which is not there in case of linked lists.

function LinkedList() {
  const Node = function(element) {
    this.element = element;
    this.next = null;
  }

  let length = 0;
  let head = null;
  
  this.append = (element) => {
    let node = new Node(element);
    let current;
    if (head === null) head = node;
    else {
      current = head;
      while (current.next) current = current.next;
      current.next = node;
    }
    length++;
  }

  this.insert = (position, element) => {
    let node = new Node(element);
    let current = head;
    let count = 1;
    while (count < position) current = current.next;
    let temp = current;
    
  }
  this.removeAt = (position) => {}
  this.remove = (element) => {}
  this.indexOf = (element) => {}
  this.isEmpty = () => {}
  this.size= () => {}
  this.toString = () => {}
  this.print = () => {}
  
}