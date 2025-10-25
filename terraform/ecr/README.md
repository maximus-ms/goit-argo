# AWS CLI конфігурація

## Як додати новий конфіг для AWS
```bash
aws configure --profile <назва_профілю>
```
Вас попросять ввести:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name
- Default output format

## Як переглянути список наявних конфігів
```bash
aws configure list-profiles
```

## Як переглянути поточний конфіг
```bash
# Перевірка активного профілю
echo $AWS_PROFILE

# Детальна інформація про поточну конфігурацію
aws configure list
```

## Як активувати конфіг за іменем
```bash
# Для поточної сесії терміналу
export AWS_PROFILE=<назва_профілю>

# Або використати профіль для окремої команди
aws s3 ls --profile <назва_профілю>
```
