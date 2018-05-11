while true; do
  ping -c1 $MYSQL_ADDRESS > /dev/null
  if [ $? -eq 0 ]; then
    break
  fi
done
echo "Successfully pinged the adress"
