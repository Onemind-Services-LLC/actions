group "default" {
  targets = ["fixture"]
}

target "fixture" {
  context = "tests/oci"
  platforms = ["linux/amd64"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom,generator=registry.onemindservices.com/docker.io/docker/buildkit-syft-scanner:stable-1@sha256:ae4f3b554449e7e25548e7d8ccc029d17357348e30c6e3df01b92bc93654d6a9"
  ]
}
