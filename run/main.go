package main

import (
	"fmt"
	"log"
	"os"

	"github.com/GrahamSpiers/icfp2024/lang"
)

func main() {
	for _, filename := range os.Args[1:] {
		bs, err := os.ReadFile(filename)
		if err != nil {
			log.Fatalf("got %v opening %s", err, filename)
		}
		fmt.Printf("%v", lang.NewICFP(string(bs)).Run())
	}
}
