import boto3

def obter_tamanhos_discos():
    ec2 = boto3.client('ec2')
    response = ec2.describe_volumes()

    gp2_size_gb = 0
    io1_size_gb = 0
    gp3_size_gb = 0
    iops_io1 = 0

    for volume in response['Volumes']:
        tamanho_gb = volume['Size']

        if 'VolumeType' in volume:
            if volume['VolumeType'] == 'gp2':
                iops_gp2 = volume.get('Iops', 0)
                if iops_gp2 <= 3000: 
                    gp2_size_gb += tamanho_gb
            elif volume['VolumeType'] == 'io1':
                io1_size_gb += tamanho_gb
                iops_io1 += volume['Iops']
            elif volume['VolumeType'] == 'gp3':
                gp3_size_gb += tamanho_gb

    return gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1

def calcular_custo(gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1):

    preco_gp2_por_gb = 0.1
    preco_io1_por_gb = 0.125
    preco_gp3_por_gb = 0.08
    preco_io1_por_iops = 0.065

    custo_gp2 = gp2_size_gb * preco_gp2_por_gb
    custo_io1 = io1_size_gb * preco_io1_por_gb + iops_io1 * preco_io1_por_iops
    custo_gp3 = gp3_size_gb * preco_gp3_por_gb

    return custo_gp2, custo_io1, custo_gp3

gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1 = obter_tamanhos_discos()
custo_gp2, custo_io1, custo_gp3 = calcular_custo(gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1)


print(f'Tamanho total para gp2: {gp2_size_gb} GB')
print(f'Tamanho total para io1: {io1_size_gb} GB, IOPS: {iops_io1}')
print(f'Tamanho total para gp3: {gp3_size_gb} GB')

print(f'\nCusto total para gp2: ${custo_gp2:.2f}')
print(f'Custo total para io1: ${custo_io1:.2f}')
print(f'Custo total para gp3: ${custo_gp3:.2f}')

valor_reduzido_io1_para_gp3 = custo_io1 - custo_gp3
print(f'\nValor reduzido ao trocar de io1 para gp3: ${valor_reduzido_io1_para_gp3:.2f}')
