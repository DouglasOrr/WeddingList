# Host requirements:

 - `jq`, `docker`, `python3`
 - `export WEDDING_LIST_DB_USER=?`
 - `export WEDDING_LIST_DB_PASSWORD=?`

# Setting up Azure resources:

    $ azure-cli

    # 1. login & check default subscription
    az login
    az account show

    # 2. create a resouce group
    az group create --location westeurope --name weddinglist

    # 3. create a container registry
    az acr create --name weddinglistacr --resource-group weddinglist --sku Basic --admin-enabled true
    az acr credential show --name weddinglistacr
    # docker login weddinglistacr.azurecr.io -u weddinglistacr -p PASSWORD
    # ./run push

    # 4. create a mysql database
    az mysql server create --resource-group weddinglist --name weddinglistdb --admin-user king --admin-password PASSWORD --performance-tier Basic --compute-units 50
    az mysql server firewall-rule create --resource-group weddinglist --server weddinglistdb --name HomeIP --start-ip-address IPADDRESS --end-ip-address IPADDRESS

# Setting up:

    ./run build
    ./run x "python -m wl.get_js"

    ./run sql-server
    ./run x "python -m wl.create_db"
    ./run x "python -m wl.bulk_insert"

    ./run run
