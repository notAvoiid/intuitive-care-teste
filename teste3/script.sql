-- OLHAR FINAL DO ARQUIVO


DROP TABLE IF EXISTS operadoras_ativas CASCADE;
DROP TABLE IF EXISTS contabeis CASCADE;

CREATE TABLE operadoras_ativas (
    registro_ans VARCHAR(6) UNIQUE NOT NULL,
    cnpj VARCHAR(14) UNIQUE,
    razao_social VARCHAR(140),
    nome_fantasia VARCHAR(140),
    modalidade VARCHAR(40),
    logradouro VARCHAR(40),
    numero VARCHAR(20),
    complemento VARCHAR(40),
    bairro VARCHAR(30),
    cidade VARCHAR(30),
    uf VARCHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(50),
    cargo_representante VARCHAR(40),
    regiao_comercializacao NUMERIC(1,0),
    data_registro_ans DATE
);

\copy operadoras_ativas FROM '/tmp/Relatorio_cadop.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';


CREATE TEMP TABLE temp_contabeis (
    data DATE,
    reg_ans BIGINT,
    cd_conta_contabil BIGINT,
    descricao VARCHAR(150),
    vl_saldo_inicial VARCHAR(20),
    vl_saldo_final VARCHAR(20)
);

\copy temp_contabeis FROM '/tmp/4T2024.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy temp_contabeis FROM '/tmp/3T2024.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy temp_contabeis FROM '/tmp/2T2024.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy temp_contabeis FROM '/tmp/1T2024.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';

\copy temp_contabeis FROM '/tmp/4T2023.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';


CREATE TABLE contabeis (
    data DATE NOT NULL,
    reg_ans BIGINT NOT NULL,
    cd_conta_contabil BIGINT NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    vl_saldo_inicial NUMERIC(18,2),
    vl_saldo_final NUMERIC(18,2)
);

INSERT INTO contabeis
SELECT
    data,
    reg_ans,
    cd_conta_contabil,
    descricao,
    NULLIF(REPLACE(vl_saldo_inicial, ',', '.'), '')::NUMERIC(18,2),
    NULLIF(REPLACE(vl_saldo_final, ',', '.'), '')::NUMERIC(18,2)
FROM temp_contabeis;

DROP TABLE temp_contabeis;

SELECT 
    o.razao_social AS operadora,
    SUM(c.vl_saldo_final - c.vl_saldo_inicial) AS total_despesas
FROM contabeis c
JOIN operadoras_ativas o 
    ON CAST(c.reg_ans AS VARCHAR) = o.registro_ans
WHERE 
    EXTRACT(YEAR FROM c.data) = 2024
    AND EXTRACT(MONTH FROM c.data) IN (10, 11, 12)  -- Filtra apenas o 4º trimestre
    AND c.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;

SELECT 
    o.razao_social AS operadora,
    SUM(c.vl_saldo_final - c.vl_saldo_inicial) AS total_despesas
FROM contabeis c
JOIN operadoras_ativas o 
    ON CAST(c.reg_ans AS VARCHAR) = o.registro_ans
WHERE EXTRACT(YEAR FROM c.data) = 2024  
    AND c.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;


/*

wget -r -np -nd -A ".zip,.csv" -P downloads https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/ && unzip 'downloads/*.zip' -d downloads && rm -f downloads/*.zip
wget -r -np -nd -A "*.csv" -P downloads https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/ && unzip 'downloads/*.zip' -d downloads && rm -f downloads/*.zip
wget -r -np -nd -A "*.zip,*.csv" -P downloads https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/ && unzip 'downloads/*.zip' -d downloads && rm -f downloads/*.zip

cp ${CAMINHO_ABSOLUTO}/downloads/Relatorio_cadop.csv /tmp/
cp ${CAMINHO_ABSOLUTO}/downloads/4T2024.csv /tmp/
cp ${CAMINHO_ABSOLUTO}/downloads/3T2024.csv /tmp/
cp ${CAMINHO_ABSOLUTO}/downloads/2T2024.csv /tmp/
cp ${CAMINHO_ABSOLUTO}/downloads/1T2024.csv /tmp/
cp ${CAMINHO_ABSOLUTO}/downloads/4T2023.csv /tmp/

*/