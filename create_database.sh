#!/bin/bash

mysql -uroot -pstrongpassword -h0.0.0.0 -P3684 <<EOF
CREATE DATABASE IF NOT EXISTS knowledge_reinforce;
EOF
