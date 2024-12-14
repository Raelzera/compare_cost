import boto3

class EC2VolumeAnalyzer:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.gp2_size_gb = 0
        self.io1_size_gb = 0
        self.gp3_size_gb = 0
        self.iops_io1 = 0

    def fetch_volumes(self):
        return self.ec2_client.describe_volumes()

    def analyze_volumes(self):
        response = self.fetch_volumes()

        for volume in response['Volumes']:
            size_gb = volume['Size']
            volume_type = volume.get('VolumeType', '')

            if volume_type == 'gp2':
                iops_gp2 = volume.get('Iops', 0)
                if iops_gp2 <= 3000: 
                    self.gp2_size_gb += size_gb
            elif volume_type == 'io1':
                self.io1_size_gb += size_gb
                self.iops_io1 += volume.get('Iops', 0)
            elif volume_type == 'gp3':
                self.gp3_size_gb += size_gb

    def get_volume_sizes(self):
        return self.gp2_size_gb, self.io1_size_gb, self.gp3_size_gb, self.iops_io1


class VolumeCostCalculator:
    def __init__(self):
        self.prices = {
            'gp2': 0.1,
            'io1': 0.125,
            'gp3': 0.08,
            'io1_iops': 0.065
        }

    def calculate_costs(self, gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1):
        cost_gp2 = gp2_size_gb * self.prices['gp2']
        cost_io1 = io1_size_gb * self.prices['io1'] + iops_io1 * self.prices['io1_iops']
        cost_gp3 = gp3_size_gb * self.prices['gp3']

        return cost_gp2, cost_io1, cost_gp3


def main():
    analyzer = EC2VolumeAnalyzer()
    analyzer.analyze_volumes()
    gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1 = analyzer.get_volume_sizes()

    calculator = VolumeCostCalculator()
    custo_gp2, custo_io1, custo_gp3 = calculator.calculate_costs(gp2_size_gb, io1_size_gb, gp3_size_gb, iops_io1)

    print(f'Tamanho total para gp2: {gp2_size_gb} GB')
    print(f'Tamanho total para io1: {io1_size_gb} GB, IOPS: {iops_io1}')
    print(f'Tamanho total para gp3: {gp3_size_gb} GB')

    print(f'\nCusto total para gp2: ${custo_gp2:.2f}')
    print(f'Custo total para io1: ${custo_io1:.2f}')
    print(f'Custo total para gp3: ${custo_gp3:.2f}')

    valor_reduzido_io1_para_gp3 = custo_io1 - custo_gp3
    print(f'\nValor reduzido ao trocar de io1 para gp3: ${valor_reduzido_io1_para_gp3:.2f}')


if __name__ == "__main__":
    main()
