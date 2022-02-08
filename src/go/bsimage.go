package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"time"
)

func build(pathDocker string) {

	cmd := exec.Command(pathDocker, "image", "build", "-f", os.Args[2], "-t", os.Args[1], ".", "--platform=linux/amd64")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		log.Fatalf("** Failed with %s\n", err)
	}
}

func scan(pathTrivy string, timestamp string) {
	cmd := exec.Command(pathTrivy, "image", "--exit-code", "1", os.Args[1])
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	outfile, errToFile := os.Create("logs_trivy_" + timestamp + ".log")
	if errToFile != nil {
		panic(errToFile)
	}
	defer outfile.Close()
	cmd.Stdout = outfile

	err := cmd.Run()
	if err != nil {
		log.Fatalf("\n\n\033[31mALERT!!! Vulnerable image!\033[0m")
	}
}

func main() {
	now := time.Now()

	docker, errDocker := exec.LookPath("docker")
	if errDocker != nil {
		log.Fatal("Docker is not installed. Go to https://www.docker.com/get-started")

	}
	pathDocker := docker

	trivy, errTrivy := exec.LookPath("trivy")
	if errTrivy != nil {
		log.Fatal("Trivy is not installed. Go to https://aquasecurity.github.io/trivy/")

	}
	pathTrivy := trivy

	fmt.Println("** BSImage (build&scan image)")
	fmt.Println("** build image and scan with trivy opensource\n")
	fmt.Println("** you can contribute to this project! visit https://github.com/pcfeduardo/bsimage\n")

	if len(os.Args) < 3 {
		// fmt.Println("Usage: " + os.Args[0] + " <image:tag> <dir_path> <dockerfile>")
		fmt.Println("Usage: " + os.Args[0] + " <image:tag> <dockerfile>")
		os.Exit(1)
	}

	build(pathDocker)
	scan(pathTrivy, now.Format("20060201150405"))
	fmt.Println("\n\n\033[32m** Congratulations! Image approved! :)\033[0m\n")
	// test()

}
