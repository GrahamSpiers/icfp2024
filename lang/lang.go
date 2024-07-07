// Functions and types for the ICFP 2024 Contest macro language (ICFP).
package lang

import (
	"fmt"
	"log"
	"strings"
)

const (
	S_ASCII    = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"
	I_BASE     = 94
	ZERO_INDEX = 33
)

var NO_ARGS = []any{}

// Op is a tree representation of an ICFP macro.
// Stores the original token.
type Op struct {
	Token string
	Args  []any
}

func (op Op) Check() error {
	if len(op.Token) == 0 {
		return fmt.Errorf("missing token")
	}
	switch op.Token[0] {
	case 'U':
		fallthrough
	case 'B':
		fallthrough
	case '?':
		fallthrough
	case 'L':
		fallthrough
	case 'v':
		break
	default:
		return fmt.Errorf("bad indicator in operation %q", op.Token)
	}
	for i, arg := range op.Args {
		if arg == nil {
			return fmt.Errorf("arg %d missing for %q", i+1, op.Token)
		}
		opArg, ok := arg.(Op)
		if !ok {
			continue
		}
		err := opArg.Check()
		if err != nil {
			return err
		}
	}
	return nil
}

func (op Op) String() string {
	ss := []string{op.Token}
	for _, arg := range op.Args {
		ss = append(ss, fmt.Sprintf("%v", arg))
	}
	return strings.Join(ss, " ")
}

// ICFPTree represents an entire ICFP macro.
type ICFP struct {
	Tree any
}

type VisitFunc func(any) bool

// Visit calls a function on each node of the tree non-recursively.
// If the function returs true the visiting returns.
func Visit(token any, fn VisitFunc) {
	stack := NewStack()
	stack.Push(token)
	for !stack.IsEmpty() {
		token := stack.Pop()
		// Visit
		if fn(token) {
			break
		}
		op, ok := token.(Op)
		if !ok {
			continue
		}
		for i := len(op.Args) - 1; i >= 0; i-- {
			stack.Push(op.Args[i])
		}
	}
}

func NewICFP(icfp string) (*ICFP, error) {
	raw := strings.Split(icfp, " ")
	var typed = []any{}
	for _, token := range raw {
		var converted any = nil
		switch token[0] {
		case 'T':
			converted = true
		case 'F':
			converted = false
		case 'I':
			converted = IToInt(token[1:])
		case 'S':
			converted = SToString(token[1:])
			//fmt.Printf("%q -> %q\n", token, converted)
		case 'U':
			converted = Op{Token: token, Args: []any{nil}}
		case 'B':
			converted = Op{Token: token, Args: []any{nil, nil}}
		case '?':
			converted = Op{Token: token, Args: []any{nil, nil, nil}}
		case 'L':
			converted = Op{Token: token, Args: []any{nil}}
		case 'v':
			converted = Op{Token: token, Args: NO_ARGS}
		default:
			return nil, fmt.Errorf("bad ICFP token %q", token)
		}
		typed = append(typed, converted)
	}
	//top, err := parse(typed)
	top, rest, err := recParse(typed)
	if err != nil {
		return nil, fmt.Errorf("got '%v' parsing %q", err, icfp)
	}
	if len(rest) > 0 {
		return nil, fmt.Errorf("unparsed tokens %v in %s", rest, icfp)
	}
	//fmt.Printf("||| %q |||\n", icfp)
	return &ICFP{
			Tree: top,
		},
		nil
}

// Size returns the number of leaves in an ICFP token tree.
func Size(token any) int {
	count := 1
	if op, ok := token.(Op); ok {
		for _, arg := range op.Args {
			count += Size(arg)
		}
	}
	return count
}

// AsString creates a string representation of an ICFP token tree.
func AsString(token any) string {
	ss := []string{}
	Visit(token, func(token any) bool {
		op, ok := token.(Op)
		switch ok {
		case true:
			ss = append(ss, op.Token)
		case false:
			ss = append(ss, fmt.Sprintf("%v", token))
		}
		return false
	})
	return strings.Join(ss, " ")
}

// recParse recursivly builds an ICFP token tree.
func recParse(typed []any) (any, []any, error) {
	if len(typed) == 0 {
		return nil, []any{}, fmt.Errorf("missing token")
	}
	token, rest := typed[0], typed[1:]
	var x, y, condition any
	var err error
	if op, ok := token.(Op); ok {
		// Op
		switch op.Token[0] {
		case 'B':
			// 2 arguments.
			x, rest, err = recParse(rest)
			if err != nil {
				return nil, []any{}, fmt.Errorf("%s[x] %v", op.Token, err)
			}
			y, rest, err = recParse(rest)
			if err != nil {
				return nil, []any{}, fmt.Errorf("%s[y] %v", op.Token, err)
			}
			op.Args[0] = x
			op.Args[1] = y
		case '?':
			// 3 arguments.
			condition, rest, err = recParse(rest)
			if err != nil {
				return nil, []any{}, fmt.Errorf("%s[?] %v", op.Token, err)
			}
			x, rest, err = recParse(rest)
			if err != nil {
				return nil, []any{}, fmt.Errorf("%s[x] %v", op.Token, err)
			}
			y, rest, err = recParse(rest)
			if err != nil {
				return nil, []any{}, fmt.Errorf("%s[y] %v", op.Token, err)
			}
			op.Args[0] = condition
			op.Args[1] = x
			op.Args[2] = y
		case 'v':
			// No arguments - do nothing.
		default:
			// U, L - 1 argument
			x, rest, err = recParse(rest)
			if err != nil {
				return nil, []any{}, fmt.Errorf("%s[x] %v", op.Token, err)
			}
			op.Args[0] = x
		}
		return op, rest, nil
	} else {
		return token, rest, nil
	}
}

// Run reduces an ICFP until it is just one token.
func (icfp *ICFP) Run() any {
	for {
		fmt.Printf("[%d] %s\n", Size(icfp.Tree), AsString(icfp.Tree))
		if IsLiteral(icfp.Tree) {
			break
		}
		icfp.Tree = RecReduce(icfp.Tree)
	}
	return icfp.Tree
}

func RecReduce(token any) any {
	op, ok := token.(Op)
	if !ok {
		return token
	}
	switch op.Token[0] {
	case 'U':
		if IsLiteral((op.Args[0])) {
			return Unary(op.Token[1:], op.Args[0])
		}
		op.Args[0] = RecReduce(op.Args[0])
		return op
	case 'B':
		if op.Token[1] == '$' {
			x, ok := op.Args[0].(Op)
			if !ok {
				log.Fatalf("literal argument %v for %q", op.Args[0], op.Token)
			}
			if x.Token[0] == 'L' {
				// Apply y to x
				return Substitute(x, op.Args[1])
			} else {
				op.Args[0] = RecReduce((op.Args[0]))
				return op
			}
		}
		if IsLiteral((op.Args[0])) {
			if IsLiteral((op.Args[1])) {
				return Binary(op.Token[1:], op.Args[0], op.Args[1])
			} else {
				op.Args[1] = RecReduce(op.Args[1])
			}
		} else {
			op.Args[0] = RecReduce((op.Args[0]))
		}
		return op
	case '?':
		if IsLiteral(op.Args[0]) {
			if op.Args[0].(bool) {
				return op.Args[1]
			} else {
				return op.Args[2]
			}
		} else {
			op.Args[0] = RecReduce(op.Args[0])
			return op
		}
	case 'L':
		return op
	case 'v':
		fallthrough
	default:
		log.Fatalf("can't reduce %q", op.Token)
		return nil
	}
}

func Substitute(el Op, y any) any {
	opStack := NewStack()
	opStack.Push(el)
	for !opStack.IsEmpty() {
		node := opStack.Pop()
		if op, ok := node.(Op); ok {
			for i, arg := range op.Args {
				if argOp, ok := arg.(Op); ok {
					if argOp.Token[0] == 'v' && argOp.Token[1:] == el.Token[1:] {
						op.Args[i] = y
					} else {
						opStack.Push(argOp)
					}
				}
			}
		}
	}
	return el.Args[0]
}

// Binary returns the result of an ICFP "B" function.
// Does not handle apply (B$).
func Binary(body string, x any, y any) any {
	switch body {
	case "+":
		return x.(int) + y.(int)
	case "-":
		return x.(int) - y.(int)
	case "*":
		return x.(int) * y.(int)
	case "/":
		return x.(int) / y.(int)
	case "%":
		return x.(int) % y.(int)
	case "<":
		return x.(int) < y.(int)
	case ">":
		return x.(int) > y.(int)
	case "=":
		switch x.(type) {
		case bool:
			return x.(bool) == y.(bool)
		case int:
			return x.(int) == y.(int)
		case string:
			return x.(string) == y.(string)
		default:
			log.Fatalf("B= mismatched types %v=%v", x, y)
		}
	case "|":
		return x.(bool) || y.(bool)
	case "&":
		return x.(bool) && y.(bool)
	case ".":
		return x.(string) + y.(string)
	case "T":
		return y.(string)[:x.(int)]
	case "D":
		return y.(string)[x.(int):]
	default:
		log.Fatalf("unhandled B operator %q", body)
		return nil
	}
	log.Fatalf("B%s undefined", body)
	return nil
}

// Unary returns the result of an ICFP "U" function.
func Unary(body string, x any) any {
	switch body {
	case "!":
		return !(x.(bool))
	case "-":
		return -(x.(int))
	case "#":
		return SToI(x.(string))
	case "$":
		return IntToString(x.(int))
	default:
		log.Fatalf("bad U body %q", body)
		return nil
	}
}

// IsLiteral returns true if this token is an ICFP non-operator.
func IsLiteral(token any) bool {
	switch token.(type) {
	case bool:
		return true
	case int:
		return true
	case string:
		return true
	default:
		return false
	}
}

func SToI(s string) int {
	i := 0
	for _, b := range []byte(s) {
		i *= I_BASE
		index := strings.IndexRune(S_ASCII, rune(b))
		i += index
	}
	return i
}

func IToS(i int) string {
	if i == 0 {
		return "!"
	}
	//fmt.Printf("%d", i)
	s := ""
	for i > 0 {
		s = string(byte(i%I_BASE)+ZERO_INDEX) + s
		i /= I_BASE
	}
	//fmt.Printf(" -> S%s\n", s)
	return s
}

func IntToString(i int) string {
	return SToString(IToS(i))
}

func STokenToString(token string) string {
	return SToString(token[1:])
}

func SToString(s string) string {
	var bs = make([]byte, len(s))
	for i, b := range []byte(s) {
		bs[i] = S_ASCII[b-ZERO_INDEX]
	}
	return string(bs)
}

func StringToS(str string) string {
	var bs = make([]byte, len(str))
	for i, ch := range str {
		index := strings.IndexRune(S_ASCII, ch)
		bs[i] = byte(ZERO_INDEX + index)
	}
	//fmt.Printf("%q -> S%q\n", str, string(bs))
	return string(bs)
}

// ITokenToInt returns converts an ICFP "I" token to an integer.
func ITokenToInt(token string) int {
	return IToInt(token[1:])
}

// IToInt converts the body portion of an ICFP "I" token to an integer.
func IToInt(s string) int {
	i := 0
	for _, b := range []byte(s) {
		i *= I_BASE
		i += int(b) - ZERO_INDEX
	}
	return i
}
