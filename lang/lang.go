package lang

import (
	"fmt"
	"log"
	"strings"
)

const (
	S_ASCII    = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\x22#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"
	I_BASE     = 94
	ZERO_INDEX = 33
)

type Op struct {
	Token string
}

type ICFP struct {
	Typed []any
}

func NewICFP(icfp string) *ICFP {
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
		default:
			converted = Op{Token: token}
		}
		typed = append(typed, converted)
	}
	return &ICFP{
		Typed: typed,
	}
}

func (icfp *ICFP) Run() any {
	tokens := icfp.Typed[:]
	for len(tokens) > 1 {
		fmt.Println(TokensToString(tokens))
		tokens = icfp.Reduce(tokens)
	}
	return tokens[0]
}

func (icfp *ICFP) Reduce(tokens []any) []any {
	hasReduced := false
	i := 0
	for !hasReduced {
		if IsLiteral(tokens[i]) {
			log.Fatalf("unexpected literal %v", tokens[i])
		}
		//fmt.Printf("%v", tokens[i])
		op := tokens[i].(Op)
		switch op.Token[0] {
		case 'U':
			if IsLiteral(tokens[i+1]) {
				uOfX := Unary(op.Token[1:], tokens[i+1])
				//fmt.Printf("#:%d  uOfX:%v", len(tokens), uOfX)
				next := append(tokens[:i], uOfX)
				//fmt.Printf("next #%d", len(next))
				tokens = append(next, tokens[i+2:]...)
				hasReduced = true
			}
		case 'B':
			if IsLiteral(tokens[i+1]) && IsLiteral(tokens[i+2]) {
				uOfXY := Binary(op.Token[1:], tokens[i+1], tokens[i+2])
				next := append(tokens[:i], uOfXY)
				tokens = append(next, tokens[i+3:]...)
				hasReduced = true
			}
		case 'L':
			log.Fatalf("L not done")
		case 'v':
			log.Fatalf("v not done")
		default:
			log.Fatalf("unexpected literal %q", tokens[i])
		}
		i += 1
	}
	return tokens
}

func TokensToString(tokens []any) string {
	ss := make([]string, len(tokens))
	for i, token := range tokens {
		switch token.(type) {
		case bool:
			if token.(bool) {
				ss[i] = "T"
			} else {
				ss[i] = "F"
			}
		case int:
			ss[i] = "I" + IToS(token.(int))
		case string:
			ss[i] = "S" + StringToS(token.(string))
		case Op:
			ss[i] = token.(Op).Token
		default:
			log.Fatalf("unknown typed token %v", token)
		}
	}
	return strings.Join(ss, " ")
}

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
			log.Fatalf("B= mismatched types")
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
	case "$":
		log.Fatalf("B$ not done")
		return nil
	default:
		log.Fatalf("unknown B operator %q", body)
		return nil
	}
	log.Fatalf("B%s undefined", body)
	return nil
}

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

/*
func EvalToken(token string) any {
	switch token[0] {
	case 'T':
		return true
	case 'F':
		return false
	case 'I':
		return ITokenToInt(token)
	case 'S':
		return STokenToString(token)
	default:
		log.Fatalf("unknown token type %q in %q", token[0], token)
		return nil
	}
}
*/

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

func ITokenToInt(token string) int {
	return IToInt(token[1:])
}

func IToInt(s string) int {
	i := 0
	for _, b := range []byte(s) {
		i *= I_BASE
		i += int(b) - ZERO_INDEX
	}
	return i
}
