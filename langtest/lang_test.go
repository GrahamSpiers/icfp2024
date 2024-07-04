package langtest

import (
	"github.com/GrahamSpiers/icfp2024/lang"
	"testing"
)

func TestTF(t *testing.T) {
	tests := [][]any{
		{"T", true},
		{"F", false},
	}
	for _, test := range tests {
		icfp := lang.NewICFP(test[0].(string))
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}

func TestI(t *testing.T) {
	tests := [][]any{
		{"I!", 0},
		{"I$", 3},
		{"I#", 2},
	}
	for _, test := range tests {
		icfp := lang.NewICFP(test[0].(string))
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
	}
	for _, test := range tests {
		icfp := lang.NewICFP(test[0].(string))
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
		{"U- U- I$", 3},
		{"U! U! T", true},
		{"U$ U# U$ U# S4%34", "test"},
	}
	for _, test := range tests {
		//t.Logf("%q\n", test[0])
		icfp := lang.NewICFP(test[0].(string))
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
		t.Logf("%q\n", test[0])
		icfp := lang.NewICFP(test[0].(string))
		result := icfp.Run()
		if test[1] != result {
			t.Fatalf("got %v expected %v from %s", result, test[1], test[0])
		}
	}
}
