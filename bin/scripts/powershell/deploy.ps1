param ( $message )
git status
pause
git add .
git commit -m "$message"
git push
npm run build
aws s3 sync build\ s3://finetune.io