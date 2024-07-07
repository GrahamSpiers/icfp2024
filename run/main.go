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
		icfp, err := lang.NewICFP(string(bs))
		if err != nil {
			log.Fatalf("error: paring %s got %v", filename, err)
		}
		fmt.Printf("%v", icfp.Run())
	}
}
