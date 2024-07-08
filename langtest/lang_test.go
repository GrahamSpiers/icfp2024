package langtest

import (
	//"fmt"
	"strings"
	"testing"

	"github.com/GrahamSpiers/icfp2024/lang"
)

func TestTF(t *testing.T) {
	tests := [][]any{
		{"T", true},
		{"F", false},
	}
	for _, test := range tests {
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestI(t *testing.T) {
	tests := [][]any{
		{"I!", 0},
		{"I\"", 1},
		{"I#", 2},
		{"I$", 3},
		{"I/6", 1337},
	}
	for _, test := range tests {
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestS(t *testing.T) {
	tests := [][]any{
		{"SB%,,/}Q/2,$_", "Hello World!"},
		{"S./", "no"},
		{"S9%3", "yes"},
		//{"S\n", "\n"},
	}
	for _, test := range tests {
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestU(t *testing.T) {
	tests := [][]any{
		{"U- I$", -3},
		{"U! T", false},
		{"U! F", true},
		{"U# S4%34", 15818151},
		{"U$ I4%34", "test"},
		{"U! U! T", true},
		{"U! U! F", false},
		{"U- U- I$", 3},
		{"U$ U# U$ U# S4%34", "test"},
	}
	for _, test := range tests {
		//fmt.Printf("%q\n", test[0])
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestB(t *testing.T) {
	tests := [][]any{
		{"B+ I# I$", 5}, // + 3 2
		{"B- I$ I#", 1}, // - 3 2
		{"B* I$ I#", 6}, // * 3 2
		{"B/ U- I( I#", -3},
		{"B% U- I( I#", -1},
		{"B< I$ I#", false},
		{"B< I# I$", true},
		{"B> I$ I#", true},
		{"B= I$ I#", false},
		{"B= T F", false},
		{"B= S./ S9%3", false},
		{"B= S9%3 S9%3", true},
		{"B| T F", true},
		{"B& F F", false},
		{"B& T T", true},
		{"B. S4% S34", "test"},
		{"B. S./ S9%3", "noyes"},
		{"BT I$ S4%34", "tes"},
		{"BD I$ S4%34", "t"},
	}
	for _, test := range tests {
		//t.Logf("%q\n", test[0])
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestSimpleReduce(t *testing.T) {
	tests := [][]any{
		{"SB%,,/}Q/2,$_", "Hello World!"},
		{"I$", 3},
		{"I#", 2},
		{"I/6", 1337},
		{"I4%34", 15818151},
		{"I!", 0},
		{"U- I$", -3},
		{"I{", 90},
		{"U- I{", -90},
		{"U! T", false},
		{"S4%34", "test"},
		{"U# S4%34", 15818151},
		{"U$ I4%34", "test"},
		{"B+ I# I$", 5},
		{"B- I$ I#", 1},
		{"B* I$ I#", 6},
		{"B/ U- I( I#", -3},
		{"B/ I( I#", 3},
		{"B% U- I( I#", -1},
		{"B% I( I#", 1},
		{"B< I$ I#", false},
		{"B< I# I$", true},
		{"B> I$ I#", true},
		{"B> I# I$", false},
		{"B= I$ I#", false},
		{"B= I$ I$", true},
		{"B| T F", true},
		{"B| T T", true},
		{"B| F F", false},
		{"B& T F", false},
		{"B& T T", true},
		{"B. S4% S34", "test"},
		{"BT I$ S4%34", "tes"},
		{"BD I$ S4%34", "t"},
		{"S./", "no"},
		{"S9%3", "yes"},
		{"? B> I# I$ S9%3 S./", "no"},
		{"? B= I# I$ S9%3 S./", "no"},
		{"? B< I# I$ S9%3 S./", "yes"},
		{"B. SB%,,/ S}Q/2,$_", "Hello World!"},
	}
	for _, test := range tests {
		//t.Logf("%q\n", test[0])
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestApply(t *testing.T) {
	tests := [][]any{
		//{"I-", 12},
		//("B+ I' I'", 12},
		{"B$ Lx I$ I!", 3},
		{"B$ Lx vx I$", 3},
		{"B$ Lx B+ vx vx I$", 6},
		{"B$ Lx B+ I$ vx I$", 6},
		{"B$ Lx B+ vx I$ I$", 6},
		//("B+ I' B* I$ I#", 12},
		//{"B* I$ I#", 6},
		//("I'", 6},
		{"B$ L\" v\" I-", 12},
		//("""B$ L" B+ v" v" I'""", 12},
		//{"''B$ L" B+ v" v" B* I$ I#''", 12},
		//{"SB%,,/}Q/2,$_", "Hello World!"},
		{"B$ L$ v$ I#", 2},
		{"B$ B$ L1 L2 v2 I! I$", 3},
		{"B$ B$ L1 L2 v1 I! I$", 0},
		{"B$ L# B$ L\" B+ v\" v\" B* I$ I# v8", 12},
		{"B$ B$ L# L$ v# SB%,,/}Q/2,$_ IK", "Hello World!"},
		{"B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK", "Hello World!"},
		//{"B$ B$ L\" B$ L# B$ v\" B$ v# v# L# B$ v\" B$ v# v# L\" L# ? B= v# I! I\" B$ L$ B+ B$ v\" v$ B$ v\" v$ B- v# I\" I%", 16},
	}
	for _, test := range tests {
		//t.Logf("%q\n", test[0])
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestCache(t *testing.T) {
	tests := [][]any{
		{"B$ Lx B+ vx vx I$", 6, 1},
		{"B$ Lx B+ I$ vx I$", 6, 0},
		{"B$ L# B$ L\" B+ v\" v\" B* I$ I# v8", 12, 1},
		//{"B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK", "Hello World!", 1},
		//{"B$ B$ L\" B$ L# B$ v\" B$ v# v# L# B$ v\" B$ v# v# L\" L# ? B= v# I! I\" B$ L$ B+ B$ v\" v$ B$ v\" v$ B- v# I\" I%", 16},
	}
	for _, test := range tests {
		//t.Logf("%q\n", test[0])
		icfp, err := lang.NewICFP(test[0].(string))
		if err != nil {
			t.Fatalf("got %v from %q", err, test[0])
		}
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
		if test[2] != icfp.CacheHits {
			t.Fatalf("got %d cache hits expected %d from %s", icfp.CacheHits, test[2], test[0])
		}
	}
}

func TestEval(t *testing.T) {
	test := "B$ B$ L\" B$ L# B$ v\" B$ v# v# L# B$ v\" B$ v# v# L\" L# ? B= v# I! I\" B$ L$ B+ B$ v\" v$ B$ v\" v$ B- v# I\" I%"
	// -> 16
	typed, err := lang.Typed(test)
	if err != nil {
		t.Fatalf("Typed got %v", err)
	}
	parsed, _, err := lang.RecParse(typed)
	if err != nil {
		t.Fatalf("RecParse got %v", err)
	}
	expected := strings.Split(test, " ") // 36 tokens
	size := lang.Size(parsed)
	if size != len(expected) {
		t.Fatalf("size wrong  got %d expected %d", size, len(expected))
	}
}

func TestRecReduce(t *testing.T) {
	//test := "B$ B$ L\" B$ L# B$ v\" B$ v# v# L# B$ v\" B$ v# v# L\" L# ? B= v# I! I\" B$ L$ B+ B$ v\" v$ B$ v\" v$ B- v# I\" I%"
	test := "B$ L# B$ L\" B+ v\" v\" B* I$ I# v8"
	icfp, _ := lang.NewICFP(test)
	count := 0
	top := icfp.Tree
	for !lang.IsLiteral(top) {
		//fmt.Printf("%d: %d\n", count, lang.Size(top))
		top = icfp.RecReduce(top)
		count += 1
	}
	if count != 5 {
		t.Fatalf("got %d reductions expected 5", count)
	}
}

/*
func TestAsString(t *testing.T) {
	test := "B$ B$ L\" B$ L# B$ v\" B$ v# v# L# B$ v\" B$ v# v# L\" L# ? B= v# I! I\" B$ L$ B+ B$ v\" v$ B$ v\" v$ B- v# I\" I%"
	icfp, err := lang.NewICFP(test)
	if err != nil {
		t.Fatalf("got %v from %q", err, test[0])
	}
	if test != lang.AsString(icfp.Tree) {
		t.Fatalf("%q != %q", lang.AsString(icfp.Tree), test)
	}
}
	B$ (
		B$ (	L#(L$ v#, (B. SB%,,/ S}Q/2,$_)
		(IK))
	((\v2 -> \v3 -> v2) ("Hello" . " World!")) 42

	((v# -> v$ -> v#) (SB%,,/ . S}Q/2,$_)) IK
	B$
*/
