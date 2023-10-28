# DSMR Monitor

> a simple monitor for DSMR readings, storing them in an Influx DB

> [!IMPORTANT]  
> This repo has been [archived](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories#).

## Rationale

When I moved into my new home, I got a "smart metering" system for electricity and gas. The meter provides usage statistics, which I wanted to monitor. 

This repo contains some basic Python code to be run on a Raspberry Pi to capture these statistics and store them in an Influx DB.

A basic web-frontend provides access to the data.

## Usage

The `Makefile` contains targets to install and run the code on a Raspberry Pi.

> [!WARNING]  
> This code is not made generic in any way. It contains configuration aspects specific to my setup, hard coded in the scripts.
