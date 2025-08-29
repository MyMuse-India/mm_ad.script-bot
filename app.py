S C:\Users\nihar\Downloads\ad-copy-regenerator> docker-compose build --no-cache
>> docker-compose up
[+] Building 378.7s (30/30) FINISHED
 => [internal] load local bake definitions                                                      0.0s 
 => => reading from stdin 1.64kB                                                                0.0s
 => [api internal] load build definition from Dockerfile                                        0.0s
 => => transferring dockerfile: 585B                                                            0.0s 
 => [web internal] load build definition from Dockerfile                                        0.0s 
 => => transferring dockerfile: 528B                                                            0.0s 
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 1)                  0.0s 
 => [worker internal] load metadata for docker.io/library/python:3.10.11-slim                   5.3s 
 => [web internal] load metadata for docker.io/library/node:20-bullseye-slim                    5.3s
 => [auth] library/python:pull token for registry-1.docker.io                                   0.0s 
 => [auth] library/node:pull token for registry-1.docker.io                                     0.0s 
 => [web internal] load .dockerignore                                                           0.0s 
 => => transferring context: 2B                                                                 0.0s 
 => [worker internal] load .dockerignore                                                        0.0s 
 => => transferring context: 2B                                                                 0.0s 
 => [web 1/6] FROM docker.io/library/node:20-bullseye-slim@sha256:f25986842968667c16e5ae74088  28.3s 
 => => resolve docker.io/library/node:20-bullseye-slim@sha256:f25986842968667c16e5ae7408817cb9  0.0s 
 => => sha256:2bd4324c30cd4042de3b98b16f9f530fe588ee435ebcb22086a970f664463c66 447B / 447B      0.9s 
 => => sha256:2edbddfbf9e37977a94166e8115fe5180300f40a0bf6b49479dd9c6b396e0b7f 1.74MB / 1.74MB  4.8s 
 => => sha256:16094b9e9c879198fc4cd75140ae105b4d4a44503715bde8953b4ad503293 41.23MB / 41.23MB  26.9s 
 => => sha256:69695de82b5f3875e375ffd63a5a3690589729246cd779ba3bcd81c12b411359 4.07kB / 4.07kB  3.4s 
 => => sha256:3e41ca17193bcd7630e4dd210602930b1f94464bdd59680bbf6654206f770 30.26MB / 30.26MB  24.1s 
 => => extracting sha256:3e41ca17193bcd7630e4dd210602930b1f94464bdd59680bbf6654206f7707b8       1.0s 
 => => extracting sha256:69695de82b5f3875e375ffd63a5a3690589729246cd779ba3bcd81c12b411359       0.0s 
 => => extracting sha256:16094b9e9c879198fc4cd75140ae105b4d4a44503715bde8953b4ad5032936c8       1.0s 
 => => extracting sha256:2edbddfbf9e37977a94166e8115fe5180300f40a0bf6b49479dd9c6b396e0b7f       0.1s 
 => => extracting sha256:2bd4324c30cd4042de3b98b16f9f530fe588ee435ebcb22086a970f664463c66       0.0s 
 => [web internal] load build context                                                           1.6s 
 => => transferring context: 57.57MB                                                            1.5s 
 => [api 1/7] FROM docker.io/library/python:3.10.11-slim@sha256:fd86924ba14682eb11a3c244f60a3  19.6s 
 => => resolve docker.io/library/python:3.10.11-slim@sha256:fd86924ba14682eb11a3c244f60a35b5df  0.0s 
 => => sha256:661be8ca6397d70bda71ffb50ca0278a4121e9276a279b922c929391ab1eeb8d 3.37MB / 3.37MB  2.8s 
 => => sha256:cf2e0f30894fffd895f2e7a379c9062bc109e99fd015273b1b805329ca366029 243B / 243B      1.4s 
 => => sha256:94970648c551e670b333e7622ae39088f0d1d365c59a18ea40666d0a75d13a 11.53MB / 11.53MB  5.4s 
 => => sha256:05c2151a829c7c573d1d540463c8928df99235dca88fba7ae468657f3a0dda73 1.08MB / 1.08MB  2.2s 
 => => sha256:f03b40093957615593f2ed142961afb6b540507e0b47e3f7626ba5e02efbbb 31.40MB / 31.40MB  9.2s 
 => => extracting sha256:f03b40093957615593f2ed142961afb6b540507e0b47e3f7626ba5e02efbbbf1       1.0s 
 => => extracting sha256:05c2151a829c7c573d1d540463c8928df99235dca88fba7ae468657f3a0dda73       0.1s 
 => => extracting sha256:94970648c551e670b333e7622ae39088f0d1d365c59a18ea40666d0a75d13a53       0.3s 
 => => extracting sha256:cf2e0f30894fffd895f2e7a379c9062bc109e99fd015273b1b805329ca366029       0.0s 
 => => extracting sha256:661be8ca6397d70bda71ffb50ca0278a4121e9276a279b922c929391ab1eeb8d       0.3s 
 => [worker internal] load build context                                                        0.1s 
 => => transferring context: 178.67kB                                                           0.0s 
 => [worker 2/7] RUN apt-get update && apt-get install -y --no-install-recommends     tessera  81.6s 
 => [web 2/6] WORKDIR /usr/src/app                                                              0.5s 
 => [web 3/6] COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./                0.1s 
 => [web 4/6] RUN if [ -f pnpm-lock.yaml ]; then corepack enable && pnpm i;     elif [ -f yarn  7.5s 
 => [web 5/6] COPY . .                                                                          0.9s 
 => [web 6/6] RUN npm run build || true                                                         2.1s 
 => [web] exporting to image                                                                    7.4s 
 => => exporting layers                                                                         3.8s 
 => => exporting manifest sha256:0df809f6c7c1977d182d6b94a74c56fccdbacd10fa85ac4dcc5573533bc89  0.0s 
 => => exporting config sha256:a4efe99e62f5909b8829fb92f128d6155d83c2fab362c8dc021ba8213ed645b  0.0s 
 => => exporting attestation manifest sha256:0106cbacd607ad708f8ad3b7df0c6ce046ae9234a08445eff  0.0s 
 => => exporting manifest list sha256:1573704847c96e141b761927f99ac534ae7812a2e0b345b9108ddf2e  0.0s 
 => => naming to docker.io/library/ad-copy-regenerator-web:latest                               0.0s 
 => => unpacking to docker.io/library/ad-copy-regenerator-web:latest                            3.4s 
 => [web] resolving provenance for metadata file                                                0.0s 
 => [api 3/7] WORKDIR /app                                                                      0.1s 
 => [api 4/7] RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu  60.0s 
 => [worker 5/7] COPY requirements.txt /app/requirements.txt                                    0.2s 
 => [worker 6/7] RUN pip install --no-cache-dir -r requirements.txt                            75.9s 
 => [worker 7/7] COPY . /app                                                                    0.2s 
 => [worker] exporting to image                                                               134.5s 
 => => exporting layers                                                                        46.5s 
 => => exporting manifest sha256:d67153271dd1899ee25609143c7cef05b7709a13dbc8527c503b6bae4e91e  0.0s 
 => => exporting config sha256:bf8bbf4c88180c2488aafe7628af2ea39a1264510c11d4f145e8a193c13331f  0.0s 
 => => exporting attestation manifest sha256:d3f1aa1015ca4e5aca9951b66822f245cf40385c3d7f9f790  0.1s 
 => => exporting manifest list sha256:cabf689a968f728498fe5851943af2b65a93ae8d65d40c441fb4ef53  0.0s 
 => => naming to docker.io/library/ad-copy-regenerator-worker:latest                            0.0s 
 => => unpacking to docker.io/library/ad-copy-regenerator-worker:latest                        87.8s 
 => [api] exporting to image                                                                  134.5s 
 => => exporting layers                                                                        46.5s 
 => => exporting manifest sha256:b70b7ee8a410977bb5329ff22d92f51d9dccc602dfb13e50b68e4ab18171f  0.0s 
 => => exporting config sha256:cee8c8e209c19b0653d1c8aa1e7fc5bb7928f30ec4b1f58cd0d20ce15eab8a8  0.0s 
 => => exporting attestation manifest sha256:720b46d53c11824e6e2014d62755914b07bc526b77195db28  0.1s 
 => => exporting manifest list sha256:e82b045028a86cb70543b91ed362b5286b9e5c34fafe79caf51d1ca1  0.0s 
 => => naming to docker.io/library/ad-copy-regenerator-api:latest                               0.0s 
 => => unpacking to docker.io/library/ad-copy-regenerator-api:latest                           87.8s 
 => [api] resolving provenance for metadata file                                                0.3s 
 => [worker] resolving provenance for metadata file                                             0.2s 
[+] Building 3/3
 ✔ ad-copy-regenerator-worker  Built                                                            0.0s 
 ✔ ad-copy-regenerator-web     Built                                                            0.0s 
 ✔ ad-copy-regenerator-api     Built                                                            0.0s 
[+] Running 21/22
 ✔ redis Pulled                                                                                19.5s 
 ✔ db Pulled                                                                                   35.0s 
 - minio Pulling                                                                               69.2s 
failed to copy: httpReadSeeker: failed open: failed to do request: Get "https://production.cloudflare.docker.com/registry-v2/docker/registry/v2/blobs/sha256/a9/a98a9d647e700e45c1d3d2e44709f23952a39c199731d84e623eb558fd5501f4/data?expires=1756456655&signature=ZrNAMEzFDXEFPzZ8d6nu%2FeaOCrQ%3D&version=2": context deadline exceeded
(venv) PS C:\Users\nihar\Downloads\ad-copy-regenerator> 
