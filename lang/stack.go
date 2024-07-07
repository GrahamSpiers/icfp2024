package lang

type Stack struct {
	contents []any
}

func NewStack() *Stack {
	return &Stack{
		contents: []any{},
	}
}

func (stack *Stack) IsEmpty() bool {
	return len(stack.contents) == 0
}

func (stack *Stack) Push(a any) {
	stack.contents = append(stack.contents, a)
}

func (stack *Stack) Pop() any {
	lm1 := len(stack.contents) - 1
	a := stack.contents[lm1]
	stack.contents = stack.contents[:lm1]
	return a
}
