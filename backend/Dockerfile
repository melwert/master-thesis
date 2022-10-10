FROM golang:1.18-alpine

WORKDIR /app

COPY go.mod ./
COPY go.sum ./

RUN go mod download && go mod verify

COPY ./ ./

RUN ls -la

RUN go build -o /backend

EXPOSE 8080

CMD [ "/backend" ]

# FROM golang:1.18

# WORKDIR /usr/src/app

# # pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
# COPY go.mod go.sum ./
# RUN go mod download && go mod verify

# COPY . .
# RUN go build -v -o /usr/local/bin/app ./...

# CMD ["app"]