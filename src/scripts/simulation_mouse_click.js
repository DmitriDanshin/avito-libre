const mouseEventOf = (eventType) => (element, x, y) => {
  const rect = element.getBoundingClientRect()

  const event = new MouseEvent(eventType, {
    view: window,
    bubbles: true,
    cancelable: true,
    clientX: rect.left + x,
    clientY: rect.top + y,
  })
  element.dispatchEvent(event)
}

function clickOnElement(element, x, y) {
  mouseEventOf('click')(element, x, y)
}

function hoverOnElement(element, x, y) {
  mouseEventOf('mousemove')(element, x, y)
  mouseEventOf('mouseover')(element, x, y)
}

const classDateName = arguments[1]
const cardElement = arguments[0]
const cardDateElement = cardElement.getElementsByClassName(classDateName)[0]

hoverOnElement(cardDateElement, 0,0)
